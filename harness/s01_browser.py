"""S01 real Chrome/CDP acceptance checks. No writes to historical evidence."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from agents.browser_checks import CDP, get_json, wait_for
from harness.cli import save
from harness.core import ROOT, snapshot

FIXTURES = r"""
window.__s01Scenario = 'real'; window.__s01Requests = []; window.__s01Aborted = false;
const browserFetch = window.fetch.bind(window);
const originalFetch = (input, options) => browserFetch(String(input).replace('http://127.0.0.1:8000', location.origin + '/__s01_api'), options);
window.fetch = (input, options = {}) => {
  const url = String(input);
  if (!/\/api\/destinations\/\d+$/.test(url)) return originalFetch(input, options);
  window.__s01Requests.push(url);
  const mode = window.__s01Scenario;
  if (mode === 'real') return originalFetch(input, options);
  if (mode === 'late' && url.endsWith('/1')) return new Promise(resolve => {
    window.__s01ReleaseA = () => originalFetch(input).then(resolve);
  });
  if (mode === 'late') return originalFetch(input, options);
  if (mode === 'slow') return new Promise((resolve, reject) => {
    window.__s01Started = performance.now();
    options.signal.addEventListener('abort', () => {
      window.__s01Aborted = true; window.__s01Duration = performance.now() - window.__s01Started;
      reject(new DOMException('Aborted', 'AbortError'));
    });
  });
  return new Promise((resolve, reject) => setTimeout(() => {
    if (mode === 'network') reject(new TypeError('Controlled network failure'));
    else resolve(new Response('{}', {status: mode === 'missing' ? 404 : 500, headers: {'Content-Type':'application/json'}}));
  }, 100));
};
"""

def main():
    checks, processes, logs = [], [], []
    cdp = None
    before = snapshot()
    record = {'spec':'001', 'started_at':datetime.now(timezone.utc).isoformat(),
              'command':['python','-B','-m','harness.s01_browser'], 'source_snapshot':before,
              'checks':checks, 'limitations':['Chrome headless via CDP, not a human screen-reader session or full WCAG audit.',
                  'Failure/late-response scenarios intercept fetch; real API success uses test-only same-origin Vite proxy to actual FastAPI port 8000. Production port 5173 was occupied; production CORS unchanged.']}
    def check(name, ac, condition, observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed})
        print(name, bool(condition), flush=True)
    def js(expression): return cdp.js(expression)
    def key(name, code, shift=False):
        for kind in ('keyDown','keyUp'):
            cdp.call('Input.dispatchKeyEvent',type=kind,key=name,code=name,windowsVirtualKeyCode=code,modifiers=8 if shift else 0, **({'text':'\r','unmodifiedText':'\r'} if name=='Enter' and kind=='keyDown' else {}))
    def ready(): return js("document.querySelectorAll('.destination-card').length === 8 && document.querySelector('.api-pill').textContent === 'API conectada'")
    def open_detail(index=0):
        js(f"document.querySelectorAll('.detail-open')[{index}].focus()")
        key('Enter',13)
        wait_for(lambda: js("!!document.querySelector('dialog[open]')"))
    def loaded(): return js("!!document.querySelector('.detail-content')")
    def close():
        js("document.querySelector('.detail-close').click()")
        wait_for(lambda: js("!document.querySelector('dialog')"))
    with tempfile.TemporaryDirectory(prefix='opita-s01-') as temporary:
        try:
            # Refuse to reuse servers which could belong to another worktree.
            for port in (8000,5187,9237):
                with socket.socket() as probe:
                    probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                      ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5187','--config','tests/s01.vite.config.mjs'],ROOT/'frontend')]
            for i,(command,cwd) in enumerate(commands):
                log=open(Path(temporary)/f'server-{i}.log','w',encoding='utf-8'); logs.append(log)
                processes.append(subprocess.Popen(command,cwd=cwd,stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            wait_for(lambda:get_json('http://127.0.0.1:8000/'))
            import urllib.request
            wait_for(lambda:urllib.request.urlopen('http://127.0.0.1:5187/',timeout=2).status==200)
            chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
            processes.append(subprocess.Popen([str(chrome),'--headless=new','--remote-debugging-port=9237',
                '--remote-allow-origins=http://localhost','--user-data-dir='+str(Path(temporary)/'chrome'),
                '--no-first-run','--no-default-browser-check','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            targets=wait_for(lambda:get_json('http://127.0.0.1:9237/json/list'))
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
            record['browser']=get_json('http://127.0.0.1:9237/json/version')['Browser']
            for method in ('Page.enable','Runtime.enable','Network.enable','Accessibility.enable'): cdp.call(method)
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source=FIXTURES)
            cdp.call('Emulation.setDeviceMetricsOverride',width=1280,height=800,deviceScaleFactor=1,mobile=False)
            cdp.call('Page.navigate',url='http://127.0.0.1:5187/')
            wait_for(ready)
            open_detail(); wait_for(loaded)
            observed=js("({title:document.querySelector('dialog h2').textContent,text:document.querySelector('dialog').textContent,requests:window.__s01Requests,focus:document.activeElement.className,count:document.querySelectorAll('dialog[open]').length})")
            check('real_api_detail_enter','AC-04',observed['title']=='Desierto de la Tatacoa' and observed['count']==1 and
                  observed['requests']==['http://127.0.0.1:8000/api/destinations/1'] and all(t in observed['text'] for t in ('Villavieja','Naturaleza','85.000','1 día','astronomía')),observed)
            tree=cdp.call('Accessibility.getFullAXTree')['nodes']
            dialogs=[n for n in tree if n.get('role',{}).get('value')=='dialog']
            check('accessible_dialog_name','AC-05',len(dialogs)==1 and dialogs[0].get('name',{}).get('value')=='Desierto de la Tatacoa',[(n.get('name',{})) for n in dialogs])
            focused=observed['focus']=='detail-close'
            key('Tab',9); focused &= js("document.activeElement.className==='detail-close'")
            key('Tab',9,True); focused &= js("document.activeElement.className==='detail-close'")
            check('focus_initial_and_tab_trap','AC-05',focused)
            # Outside programmatic focus must be blocked by native modal inertness.
            js("document.querySelector('.detail-open').focus()")
            check('modal_background_inert','AC-05',js("document.activeElement.className==='detail-close'"))
            key('Escape',27); wait_for(lambda:js("!document.querySelector('dialog')"))
            check('escape_restores_focus','AC-05',js("document.activeElement===document.querySelector('.detail-open')"))
            open_detail(); wait_for(loaded); close()
            check('close_button_restores_focus','AC-05',js("document.activeElement===document.querySelector('.detail-open')"))
            for mode in ('network','server','slow'):
                js(f"window.__s01Scenario='{mode}'")
                open_detail()
                check(mode+'_loading_announced','AC-07',js("document.querySelector('[role=status]').textContent.includes('Cargando')"))
                wait_for(loaded,timeout=8)
                observed=js("({text:document.querySelector('dialog').textContent,aborted:window.__s01Aborted,duration:window.__s01Duration})")
                check(mode+'_catalogue_fallback','AC-07','Datos del catálogo; detalle no disponible' in observed['text'] and 'Villavieja' in observed['text'],observed)
                if mode=='slow': check('deadline_aborts_request','AC-07',observed['aborted'] and 4900<=observed['duration']<=6000,observed['duration'])
                close()
            js("window.__s01Scenario='missing'"); open_detail()
            wait_for(lambda:js("document.querySelector('dialog h2').textContent==='Destino no encontrado'"))
            check('404_no_catalogue_fallback','AC-08',js("!document.querySelector('.detail-content') && !document.querySelector('dialog').textContent.includes('Villavieja')")); close()
            js("window.__s01Scenario='late'"); open_detail(0)
            wait_for(lambda:js("typeof window.__s01ReleaseA==='function'")); close()
            open_detail(1); wait_for(loaded)
            js("window.__s01ReleaseA()")
            time.sleep(.3)
            check('late_response_does_not_overwrite_B','AC-09',js("document.querySelector('dialog h2').textContent.includes('San Agustín') && !document.querySelector('dialog').textContent.includes('Villavieja')"));close()
            js("window.__s01Scenario='real'")
            js("document.querySelector('#municipality-filter').value='Neiva';document.querySelector('#municipality-filter').dispatchEvent(new Event('change',{bubbles:true}))")
            js("[...document.querySelectorAll('.filter')].find(b=>b.textContent==='Cultura').click()")
            js("(()=>{const el=document.querySelector('.searchbox input');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,'Malecón');el.dispatchEvent(new Event('input',{bubbles:true}));})()")
            wait_for(lambda:js("document.querySelectorAll('.destination-card').length===1"))
            for width in (360,1280):
                cdp.call('Emulation.setDeviceMetricsOverride',width=width,height=800,deviceScaleFactor=1,mobile=width==360)
                open_detail(); wait_for(loaded)
                observed=js("(()=>{const d=document.querySelector('dialog');const r=d.getBoundingClientRect();d.scrollTop=d.scrollHeight;return {fits:d.scrollWidth<=d.clientWidth+1&&r.width<=innerWidth&&r.height<=innerHeight,fields:d.querySelectorAll('dd').length,tags:d.querySelectorAll('li').length};})()")
                check(f'responsive_{width}','AC-10',observed['fits'] and observed['fields']==4 and observed['tags']>0,observed);close()
                check(f'filters_preserved_{width}','AC-10',js("document.querySelector('#municipality-filter').value==='Neiva' && document.querySelector('.searchbox input').value==='Malecón' && document.querySelector('.filter.active').textContent==='Cultura' && document.querySelectorAll('.destination-card').length===1"))
            # Existing recommendations still work against the actual API.
            js("document.querySelector('.planner-form').requestSubmit()")
            wait_for(lambda:js("!!document.querySelector('.result-item')"))
            check('existing_recommendations_real_api','regression',True)
            cdp.call('Network.setBlockedURLs',urls=['http://127.0.0.1:5187/__s01_api/*','*images.unsplash.com*'])
            cdp.call('Page.reload')
            wait_for(lambda:js("document.querySelector('.api-pill').textContent==='Modo demostración'"))
            open_detail();wait_for(loaded)
            check('offline_demo_detail','AC-06',js("document.querySelector('dialog').textContent.includes('Modo demostración') && document.querySelector('dialog').textContent.includes('Villavieja') && window.__s01Requests.length===0"));close()
            check('no_runtime_exceptions','regression',not cdp.exceptions,cdp.exceptions)
        except Exception as exc:
            record['error']={'type':type(exc).__name__,'message':str(exc)}
            if cdp:
                try:
                    record['diagnostic']=js("({url:location.href,status:document.querySelector('.api-pill')?.textContent,cards:document.querySelectorAll('.destination-card').length,dialog:document.querySelector('dialog')?.textContent,body:document.body.innerText.slice(0,1500)})")
                    record['runtime_exceptions']=cdp.exceptions
                except Exception: pass
        finally:
            if cdp:
                try: cdp.ws.close()
                except Exception: pass
            for process in reversed(processes):
                if process.poll() is None:
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
                    try: process.wait(timeout=10)
                    except subprocess.TimeoutExpired: pass
            for log in logs: log.close()
            record['server_logs']=[(Path(temporary)/f'server-{i}.log').read_text(encoding='utf-8',errors='replace') for i in range(len(logs))]
            record['finished_at']=datetime.now(timezone.utc).isoformat()
            record['source_unchanged_during_run']=snapshot()==before
            record['passed']=not record.get('error') and all(c['passed'] for c in checks) and record['source_unchanged_during_run']
            save(record,'s01-browser')
    return 0 if record['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
