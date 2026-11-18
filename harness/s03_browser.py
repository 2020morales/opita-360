"""S03 real Chrome/CDP tests, unique reports and owned-process cleanup."""
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
    report={'spec':'003','started_at':datetime.now(timezone.utc).isoformat(),
            'command':['python','-B','-m','harness.s03_browser'],'source_snapshot':before,'checks':checks,
            'limitations':['Chrome headless/CDP, not human screen-reader or full WCAG audit.',
                'API success uses a test-only same-origin proxy in Vite 5189 to real FastAPI 8000; production API URL and CORS unchanged.',
                'Offline scenario blocks API requests; no remote production deployment tested.']}
    def js(expr): return cdp.js(expr)
    def check(name,ac,condition,observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed});print(name,bool(condition),flush=True)
    def set_input(selector,value):
        import json
        js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,{json.dumps(value)});el.dispatchEvent(new Event('input',{{bubbles:true}}));}})()")
    def cards():return js("document.querySelectorAll('.destination-card').length")
    def expect_count(n):wait_for(lambda:cards()==n)
    def heart(index):js(f"document.querySelectorAll('.heart')[{index}].click()")
    def key(name,code):
        for kind in ('keyDown','keyUp'):
            cdp.call('Input.dispatchKeyEvent',type=kind,key=name,code='Space' if name==' ' else name,windowsVirtualKeyCode=code,
                **({'text':'\r','unmodifiedText':'\r'} if name=='Enter' and kind=='keyDown' else {}))
    def navigate(scenario=''):
        cdp.call('Page.navigate',url='http://127.0.0.1:5189/?scenario='+scenario)
        wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"));expect_count(8)
    def marked(index):return js(f"document.querySelectorAll('.heart')[{index}].getAttribute('aria-pressed')==='true'")
    with tempfile.TemporaryDirectory(prefix='opita-s03-') as tmp:
        try:
            for port in (8000,5189,9239):
                with socket.socket() as probe:probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5189','--config','tests/s03.vite.config.mjs'],ROOT/'frontend')]
            for i,(cmd,cwd) in enumerate(commands):
                stream=open(Path(tmp)/f'server-{i}.log','w',encoding='utf-8');logs.append(stream)
                processes.append(subprocess.Popen(cmd,cwd=cwd,stdout=stream,stderr=stream,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            wait_for(lambda:get_json('http://127.0.0.1:8000/'))
            wait_for(lambda:urllib.request.urlopen('http://127.0.0.1:5189/',timeout=2).status==200)
            chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
            processes.append(subprocess.Popen([str(chrome),'--headless=new','--remote-debugging-port=9239','--remote-allow-origins=http://localhost',
                '--user-data-dir='+str(Path(tmp)/'chrome'),'--no-first-run','--no-default-browser-check','about:blank'],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            targets=wait_for(lambda:get_json('http://127.0.0.1:9239/json/list'))
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
            report['browser']=get_json('http://127.0.0.1:9239/json/version')['Browser']
            for method in ('Page.enable','Runtime.enable','Network.enable','Accessibility.enable'):cdp.call(method)
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source=r"""
const key='opita360:favorites:v1'; const mode=new URLSearchParams(location.search).get('scenario');
const rawSet=Storage.prototype.setItem,rawGet=Storage.prototype.getItem;
window.__favoriteWrites=[];
if(mode==='seeded') rawSet.call(localStorage,key,JSON.stringify({version:1,ids:[3,999]}));
if(mode==='corrupt') rawSet.call(localStorage,key,'{broken');
if(mode==='manipulated') rawSet.call(localStorage,key,JSON.stringify({version:1,ids:[3,3,-1,0,'2',null,{},999]}));
rawSet.call(localStorage,'other-application-key','unchanged');
Storage.prototype.setItem=function(k,v){
 if(k===key){window.__favoriteWrites.push(v);if(mode==='writeblocked') throw new DOMException('Quota','QuotaExceededError');}
 return rawSet.call(this,k,v);
};
Storage.prototype.getItem=function(k){if(k===key&&mode==='readblocked')throw new DOMException('Denied','SecurityError');return rawGet.call(this,k);};
if(mode==='getterblocked')Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied','SecurityError');}});
const originalFetch=window.fetch.bind(window);window.fetch=(url,options)=>originalFetch(String(url).replace('http://127.0.0.1:8000',location.origin+'/__s03_api'),options);
""")
            cdp.call('Emulation.setDeviceMetricsOverride',width=1280,height=800,deviceScaleFactor=1,mobile=False)
            navigate()
            check('real_api_catalogue','regression',True,8)
            check('initialization_no_write','AC-01',js("window.__favoriteWrites.length===0"))
            heart(2);wait_for(lambda:marked(2))
            check('save_ID3_only','AC-01',js("JSON.stringify(JSON.parse(localStorage.getItem('opita360:favorites:v1')))===JSON.stringify({version:1,ids:[3]})"))
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"));expect_count(8)
            check('reload_preserves_ID3_without_initial_write','AC-01',marked(2) and js("window.__favoriteWrites.length===0"))
            js("document.querySelector('#only-favorites').click()");expect_count(1)
            check('only_favorites_shows_saved_destination','AC-01',js("document.querySelector('.destination-title h3').textContent.includes('Malecón')"))
            js("document.querySelector('.heart').focus()");key('Enter',13);expect_count(0)
            check('remove_in_only_mode_moves_focus','AC-02',js("document.activeElement===document.querySelector('#only-favorites') && JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids.length===0"))
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"));expect_count(8)
            js("document.querySelector('#only-favorites').click()");expect_count(0)
            check('removal_survives_reload','AC-02',True)
            navigate('seeded')
            check('existing_and_unknown_IDs_not_overwritten','AC-01',marked(2) and js("window.__favoriteWrites.length===0 && JSON.stringify(JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids)==='[3,999]'"))
            js("document.querySelector('#municipality-filter').value='Neiva';document.querySelector('#municipality-filter').dispatchEvent(new Event('change',{bubbles:true}))")
            js("[...document.querySelectorAll('.filter')].find(b=>b.textContent==='Cultura').click()")
            set_input('.searchbox input','Malecón');expect_count(1)
            js("document.querySelector('#only-favorites').click()");expect_count(1)
            check('favorites_AND_existing_filters','regression',js("document.querySelector('#municipality-filter').value==='Neiva' && document.querySelector('.filter.active').textContent==='Cultura' && document.querySelector('.searchbox input').value==='Malecón'"))
            heart(0);expect_count(0)
            check('unknown_ID_retained_and_filters_unchanged','AC-02',js("JSON.stringify(JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids)==='[999]' && document.querySelector('#municipality-filter').value==='Neiva' && document.querySelector('.searchbox input').value==='Malecón'"))
            js("document.querySelector('#only-favorites').click()");expect_count(1)
            check('leaving_only_mode_restores_filtered_results','regression',True)
            navigate('corrupt')
            check('corrupt_JSON_recovers_without_write','AC-03',js("document.querySelectorAll('.heart[aria-pressed=true]').length===0 && !!document.querySelector('.favorites-notice') && window.__favoriteWrites.length===0 && localStorage.getItem('opita360:favorites:v1')==='{broken'"))
            heart(0);wait_for(lambda:marked(0))
            check('corrupt_storage_replaced_only_after_user_action','AC-03',js("JSON.stringify(JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids)==='[1]' && window.__favoriteWrites.length===1"))
            navigate('manipulated')
            check('manipulated_IDs_safe_no_initial_overwrite','AC-03',marked(2) and js("document.querySelectorAll('.heart[aria-pressed=true]').length===1 && window.__favoriteWrites.length===0"))
            heart(0);wait_for(lambda:marked(0))
            check('user_write_sanitizes_and_preserves_unknown_ID','AC-03',js("JSON.stringify(JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids)==='[3,999,1]'"))
            for mode in ('getterblocked','readblocked','writeblocked'):
                navigate(mode);heart(1);wait_for(lambda:marked(1))
                check(mode+'_session_toggle_and_notice','AC-04',js("document.querySelector('.favorites-notice').textContent.includes('Solo esta sesión')"))
                heart(1);wait_for(lambda:not marked(1))
                check(mode+'_session_removal_works','AC-04',True)
            navigate('seeded')
            js("document.querySelector('.heart').focus()");key('Enter',13);wait_for(lambda:marked(0))
            check('Enter_updates_accessible_state_and_keeps_focus','AC-05',js("document.activeElement===document.querySelector('.heart') && document.querySelector('.heart').getAttribute('aria-label').startsWith('Quitar')"))
            key(' ',32);wait_for(lambda:not marked(0))
            check('Space_updates_accessible_state_and_keeps_focus','AC-05',js("document.activeElement===document.querySelector('.heart') && document.querySelector('.heart').getAttribute('aria-label').startsWith('Guardar')"))
            tree=cdp.call('Accessibility.getFullAXTree')['nodes']
            check('AX_toggle_button_name_and_pressed_state','AC-05',any(n.get('role',{}).get('value')=='button' and str(n.get('name',{}).get('value','')).startswith('Guardar Desierto') and any(v.get('name')=='pressed' and v.get('value',{}).get('value') in (False,'false') for v in n.get('properties',[])) for n in tree))
            check('other_storage_key_untouched','regression',js("localStorage.getItem('other-application-key')==='unchanged'"))
            js("document.querySelector('.planner-form').requestSubmit()")
            wait_for(lambda:js("!!document.querySelector('.result-item')"));check('real_api_recommendations_unchanged','regression',True)
            cdp.call('Network.setBlockedURLs',urls=['http://127.0.0.1:5189/__s03_api/*','*images.unsplash.com*'])
            cdp.call('Page.navigate',url='http://127.0.0.1:5189/?scenario=seeded')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"));expect_count(8)
            js("document.querySelector('#only-favorites').click()");expect_count(1)
            check('demo_uses_same_favorite_IDs','AC-01',js("document.querySelector('.destination-title h3').textContent.includes('Malecón')"))
            heart(0);expect_count(0);check('demo_remove_and_focus','AC-02',js("document.activeElement===document.querySelector('#only-favorites')"))
            check('no_runtime_exceptions','regression',not cdp.exceptions,cdp.exceptions)
        except Exception as exc:
            report['error']={'type':type(exc).__name__,'message':str(exc)}
            if cdp:
                try:report['diagnostic']=js("({cost:document.querySelector('.favorites-notice')?.textContent,cards:document.querySelectorAll('.destination-card').length,body:document.body.innerText.slice(0,700)})")
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
            save(report,'s03-browser')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
