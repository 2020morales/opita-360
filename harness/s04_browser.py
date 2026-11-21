"""S04 real Chrome/CDP tests, unique reports and owned-process cleanup."""
from datetime import datetime, timezone
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib.request
from agents.browser_checks import CDP, get_json, wait_for
from harness.cli import save
from harness.core import ROOT, snapshot

def main():
    before=snapshot(); checks=[]; processes=[]; logs=[]; cdp=None
    report={'spec':'004','started_at':datetime.now(timezone.utc).isoformat(),
            'command':['python','-B','-m','harness.s04_browser'],'source_snapshot':before,'checks':checks,
            'limitations':['Chrome headless/CDP, not human screen-reader or full WCAG audit.',
                'API success uses a test-only same-origin proxy in Vite 5190 to real FastAPI 8000; production API URL and CORS unchanged.',
                'Offline scenario blocks API requests; no remote production deployment tested.']}
    def js(expr): return cdp.js(expr)
    def check(name,ac,condition,observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed});print(name,bool(condition),flush=True)
    def set_input(selector,value):
        import json
        js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,{json.dumps(value)});el.dispatchEvent(new Event('input',{{bubbles:true}}));}})()")
    def select(selector,value):
        import json
        js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});el.value={json.dumps(value)};el.dispatchEvent(new Event('change',{{bubbles:true}}));}})()")
    def submit():
        target=js('window.__recRequests.length')+1
        js("document.querySelector('.planner-form').requestSubmit()")
        wait_for(lambda:js(f"window.__recFinished>={target} && !document.querySelector('.submit-button').disabled"))
    def municipalities():return js("[...document.querySelectorAll('.result-details p')].map(e=>e.textContent.split('·')[0].trim())")
    def missing_option():js("(()=>{const o=document.createElement('option');o.value='Municipio sin destinos';o.textContent='Municipio sin destinos (fixture de desincronización)';document.querySelector('#trip-municipality').appendChild(o);})()")
    def key(name,code):
        for kind in ('keyDown','keyUp'):cdp.call('Input.dispatchKeyEvent',type=kind,key=name,code=name,windowsVirtualKeyCode=code)
    with tempfile.TemporaryDirectory(prefix='opita-s04-') as tmp:
        try:
            for port in (8000,5190,9240):
                with socket.socket() as probe:probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5190','--config','tests/s04.vite.config.mjs'],ROOT/'frontend')]
            for i,(cmd,cwd) in enumerate(commands):
                stream=open(Path(tmp)/f'server-{i}.log','w',encoding='utf-8');logs.append(stream)
                processes.append(subprocess.Popen(cmd,cwd=cwd,stdout=stream,stderr=stream,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            wait_for(lambda:get_json('http://127.0.0.1:8000/'))
            wait_for(lambda:urllib.request.urlopen('http://127.0.0.1:5190/',timeout=2).status==200)
            chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
            processes.append(subprocess.Popen([str(chrome),'--headless=new','--remote-debugging-port=9240','--remote-allow-origins=http://localhost',
                '--user-data-dir='+str(Path(tmp)/'chrome'),'--no-first-run','--no-default-browser-check','about:blank'],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            targets=wait_for(lambda:get_json('http://127.0.0.1:9240/json/list'))
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
            report['browser']=get_json('http://127.0.0.1:9240/json/version')['Browser']
            for method in ('Page.enable','Runtime.enable','Network.enable','Accessibility.enable'):cdp.call(method)
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source="""
window.__recRequests=[];window.__recFinished=0;
const originalFetch=window.fetch.bind(window);
window.fetch=async (url,options)=>{
 const rec=String(url).endsWith('/api/recommendations');
 if(rec)window.__recRequests.push(JSON.parse(options.body));
 try{return await originalFetch(String(url).replace('http://127.0.0.1:8000',location.origin+'/__s04_api'),options);}
 finally{if(rec)window.__recFinished++;}
};
""")
            cdp.call('Emulation.setDeviceMetricsOverride',width=1280,height=800,deviceScaleFactor=1,mobile=False)
            cdp.call('Page.navigate',url='http://127.0.0.1:5190/')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada' && document.querySelectorAll('.destination-card').length===8"))
            check('real_api_catalogue','regression',True)
            select('#municipality-filter','Rivera');wait_for(lambda:js("document.querySelectorAll('.destination-card').length===1"))
            select('#trip-municipality','Neiva');submit()
            observed=municipalities()
            check('connected_Neiva_payload_and_restricted_recovery','AC-02',len(observed)==2 and all(v=='Neiva' for v in observed) and js("window.__recRequests.at(-1).municipality==='Neiva'"),observed)
            check('planner_selector_independent_of_catalogue','AC-05',js("document.querySelector('#municipality-filter').value==='Rivera' && document.querySelectorAll('.destination-card').length===1 && document.querySelector('#trip-municipality').value==='Neiva'"))
            select('#trip-municipality','');submit()
            check('Todos_omits_field_and_preserves_legacy_result','AC-01',js("!Object.hasOwn(window.__recRequests.at(-1),'municipality')") and municipalities()==['Rivera','San Agustín'],municipalities())
            missing_option();select('#trip-municipality','Municipio sin destinos');submit()
            check('unknown_API_empty_no_fallback','AC-03',len(municipalities())==0 and js("!!document.querySelector('.result-empty') && document.querySelector('.result-total b').textContent.includes('0') && document.querySelector('.result-notice').textContent.includes('No hay destinos')"))
            select('#trip-municipality','Neiva');set_input('#budget','0');submit()
            check('existing_first_stop_budget_exception_kept','AC-01',municipalities()==['Neiva'] and js("document.querySelector('.result-total b').textContent.includes('35.000')"))
            tree=cdp.call('Accessibility.getFullAXTree')['nodes']
            check('selector_has_accessible_name','AC-05',any(n.get('role',{}).get('value')=='combobox' and n.get('name',{}).get('value')=='Municipio de la propuesta' for n in tree))
            js("document.querySelector('#trip-municipality').focus()");key('ArrowDown',40)
            wait_for(lambda:js("document.querySelector('#trip-municipality').value!=='Neiva'"))
            check('selector_operable_with_keyboard','AC-05',js("document.activeElement===document.querySelector('#trip-municipality')"))
            for width in (360,1280):
                cdp.call('Emulation.setDeviceMetricsOverride',width=width,height=800,deviceScaleFactor=1,mobile=width==360)
                check('selector_fits_'+str(width),'accessibility',js("(()=>{const r=document.querySelector('#trip-municipality').getBoundingClientRect();return r.left>=0 && r.right<=innerWidth;})()"))
            cdp.call('Network.setBlockedURLs',urls=['http://127.0.0.1:5190/__s04_api/*','*images.unsplash.com*'])
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"))
            select('#municipality-filter','Rivera');select('#trip-municipality','Neiva');submit()
            observed=municipalities()
            check('demo_Neiva_recovery_never_escapes','AC-04',len(observed)==2 and all(v=='Neiva' for v in observed) and js("document.querySelector('.result-notice').textContent.includes('demostración')"),observed)
            check('demo_selector_keeps_catalogue_independent','AC-05',js("document.querySelector('#municipality-filter').value==='Rivera' && document.querySelectorAll('.destination-card').length===1"))
            missing_option();select('#trip-municipality','Municipio sin destinos');submit()
            check('demo_unknown_empty_no_global_fallback','AC-04',len(municipalities())==0 and js("!!document.querySelector('.result-empty') && document.querySelector('.result-notice').textContent.includes('No hay destinos')"))
            select('#trip-municipality','');submit()
            check('demo_Todos_recovers_legacy_flow','AC-04',municipalities()==['Rivera','San Agustín'] and js("!Object.hasOwn(window.__recRequests.at(-1),'municipality')"),municipalities())
            check('no_runtime_exceptions','regression',not cdp.exceptions,cdp.exceptions)
        except Exception as exc:
            report['error']={'type':type(exc).__name__,'message':str(exc)}
            if cdp:
                try:report['diagnostic']=js("({selection:document.querySelector('#trip-municipality')?.value,cards:document.querySelectorAll('.destination-card').length,body:document.body.innerText.slice(0,700)})")
                except Exception:pass
        finally:
            if cdp:
                try:cdp.ws.close()
                except Exception:pass
            for process in reversed(processes):
                if process.poll() is None:
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:pass
            for stream in logs:stream.close()
            report['server_logs']=[(Path(tmp)/f'server-{i}.log').read_text(encoding='utf-8',errors='replace') for i in range(len(logs))]
            report['finished_at']=datetime.now(timezone.utc).isoformat();report['source_unchanged_during_run']=snapshot()==before
            report['passed']=not report.get('error') and all(c['passed'] for c in checks) and report['source_unchanged_during_run']
            save(report,'s04-browser')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
