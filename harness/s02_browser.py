"""S02 real Chrome/CDP tests, unique reports and owned-process cleanup."""
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
    report={'spec':'002','started_at':datetime.now(timezone.utc).isoformat(),
            'command':['python','-B','-m','harness.s02_browser'],'source_snapshot':before,'checks':checks,
            'limitations':['Chrome headless/CDP, not human screen-reader or full WCAG audit.',
                'API success uses a test-only same-origin proxy in Vite 5188 to real FastAPI 8000; production API URL and CORS unchanged.',
                'Offline scenario blocks API requests; no remote production deployment tested.']}
    def js(expr): return cdp.js(expr)
    def check(name,ac,condition,observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed});print(name,bool(condition),flush=True)
    def set_input(selector,value):
        import json
        js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,{json.dumps(value)});el.dispatchEvent(new Event('input',{{bubbles:true}}));}})()")
    def apply(value):
        set_input('#max-cost',value);js("document.querySelector('.cost-filter').requestSubmit()")
    def cards():return js("document.querySelectorAll('.destination-card').length")
    def clear():js("document.querySelector('.cost-filter button[type=button]').click()")
    def expect_count(n):wait_for(lambda:cards()==n)
    with tempfile.TemporaryDirectory(prefix='opita-s02-') as tmp:
        try:
            for port in (8000,5188,9238):
                with socket.socket() as probe:probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5188','--config','tests/s02.vite.config.mjs'],ROOT/'frontend')]
            for i,(cmd,cwd) in enumerate(commands):
                stream=open(Path(tmp)/f'server-{i}.log','w',encoding='utf-8');logs.append(stream)
                processes.append(subprocess.Popen(cmd,cwd=cwd,stdout=stream,stderr=stream,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            wait_for(lambda:get_json('http://127.0.0.1:8000/'))
            wait_for(lambda:urllib.request.urlopen('http://127.0.0.1:5188/',timeout=2).status==200)
            chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
            processes.append(subprocess.Popen([str(chrome),'--headless=new','--remote-debugging-port=9238','--remote-allow-origins=http://localhost',
                '--user-data-dir='+str(Path(tmp)/'chrome'),'--no-first-run','--no-default-browser-check','about:blank'],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            targets=wait_for(lambda:get_json('http://127.0.0.1:9238/json/list'))
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
            report['browser']=get_json('http://127.0.0.1:9238/json/version')['Browser']
            for method in ('Page.enable','Runtime.enable','Network.enable','Accessibility.enable'):cdp.call(method)
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source="const originalFetch=window.fetch.bind(window);window.fetch=(url,options)=>originalFetch(String(url).replace('http://127.0.0.1:8000',location.origin+'/__s02_api'),options);")
            cdp.call('Emulation.setDeviceMetricsOverride',width=1280,height=800,deviceScaleFactor=1,mobile=False)
            cdp.call('Page.navigate',url='http://127.0.0.1:5188/')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"));expect_count(8)
            check('real_api_catalogue','regression',True,8)
            apply('35000');expect_count(1)
            check('inclusive_boundary_35000','AC-01',js("document.querySelector('.destination-title h3').textContent.includes('Malecón')"))
            for value in ('-1','abc','35abc'):
                apply(value);wait_for(lambda:js("!!document.querySelector('#max-cost-error')"))
                check('invalid_'+value+'_keeps_last_valid','AC-04',cards()==1 and js("document.querySelector('#max-cost').getAttribute('aria-invalid')==='true' && document.querySelector('.cost-filter-status').textContent.includes('35.000')"))
            tree=cdp.call('Accessibility.getFullAXTree')['nodes']
            check('accessible_cost_label','accessibility',any('Costo máximo por destino' in str(n.get('name',{}).get('value','')) and n.get('role',{}).get('value')=='textbox' for n in tree))
            clear();expect_count(8)
            js("document.querySelector('#municipality-filter').value='Neiva';document.querySelector('#municipality-filter').dispatchEvent(new Event('change',{bubbles:true}))")
            js("[...document.querySelectorAll('.filter')].find(b=>b.textContent==='Cultura').click()")
            set_input('.searchbox input','Centro');expect_count(1)
            apply('35000');expect_count(0)
            check('four_filters_AND','AC-02',True)
            apply('');expect_count(1)
            check('empty_preserves_other_filters','AC-02',js("document.querySelector('#municipality-filter').value==='Neiva' && document.querySelector('.filter.active').textContent==='Cultura' && document.querySelector('.searchbox input').value==='Centro'"))
            apply('0');expect_count(0)
            check('zero_empty_and_recovery_message','AC-03',js("document.querySelector('.empty-state').textContent.includes('límite de costo') && document.querySelector('.cost-filter-status').textContent.includes('0')"))
            clear();expect_count(1)
            check('recovery_preserves_municipality_search_category','AC-03',js("document.querySelector('#municipality-filter').value==='Neiva' && document.querySelector('.searchbox input').value==='Centro' && document.querySelector('.filter.active').textContent==='Cultura'"))
            for width in (360,1280):
                cdp.call('Emulation.setDeviceMetricsOverride',width=width,height=800,deviceScaleFactor=1,mobile=width==360)
                check('cost_controls_fit_'+str(width),'accessibility',js("[...document.querySelectorAll('.cost-filter input,.cost-filter button')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0 && r.right<=innerWidth;})"))
            set_input('#max-cost','45000');js("document.querySelector('#max-cost').focus()")
            for kind in ('keyDown','keyUp'):
                cdp.call('Input.dispatchKeyEvent',type=kind,key='Enter',code='Enter',windowsVirtualKeyCode=13,**({'text':'\r','unmodifiedText':'\r'} if kind=='keyDown' else {}))
            wait_for(lambda:js("document.querySelector('.cost-filter-status').textContent.includes('45.000')"))
            check('keyboard_enter_applies','accessibility',True)
            js("document.querySelector('.planner-form').requestSubmit()")
            wait_for(lambda:js("!!document.querySelector('.result-item')"));check('recommendations_real_api_unchanged','regression',True)
            cdp.call('Network.setBlockedURLs',urls=['http://127.0.0.1:5188/__s02_api/*','*images.unsplash.com*'])
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"));expect_count(8)
            apply('35000');expect_count(1);check('demo_inclusive_filter','AC-01',js("document.querySelector('.destination-title h3').textContent.includes('Malecón')"))
            apply('0');expect_count(0);check('demo_zero_empty','AC-03',True)
            clear();expect_count(8);check('demo_recovery','AC-03',True)
            check('no_runtime_exceptions','regression',not cdp.exceptions,cdp.exceptions)
        except Exception as exc:
            report['error']={'type':type(exc).__name__,'message':str(exc)}
            if cdp:
                try:report['diagnostic']=js("({cost:document.querySelector('.cost-filter-status')?.textContent,cards:document.querySelectorAll('.destination-card').length,body:document.body.innerText.slice(0,700)})")
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
            save(report,'s02-browser')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
