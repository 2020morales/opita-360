"""S05 real Chrome/CDP tests, unique reports and owned-process cleanup."""
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
    report={'spec':'005','started_at':datetime.now(timezone.utc).isoformat(),
            'command':['python','-B','-m','harness.s05_browser'],'source_snapshot':before,'checks':checks,
            'limitations':['Chrome headless/CDP, not human screen-reader or full WCAG audit.',
                'API success uses a test-only same-origin proxy in Vite 5190 to real FastAPI 8000; production API URL and CORS unchanged.',
                'Offline scenario blocks API requests; no remote production deployment tested.']}
    def js(expr): return cdp.js(expr)
    def check(name,ac,condition,observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed});print(name,bool(condition),flush=True)
    with tempfile.TemporaryDirectory(prefix='opita-s05-') as tmp:
        try:
            for port in (8000,5190,9240):
                with socket.socket() as probe:probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5190','--config','tests/s05.vite.config.mjs'],ROOT/'frontend')]
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
            import json, time
            downloads=Path(tmp)/'downloads';downloads.mkdir()
            cdp.call('Browser.setDownloadBehavior',behavior='allow',downloadPath=str(downloads),eventsEnabled=True)
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source="""
window.__exportClicks=0;window.__anchorClicks=0;document.addEventListener('click',e=>{if(e.target.closest('.export-button'))window.__exportClicks++;if(e.target.tagName==='A'&&e.target.download)window.__anchorClicks++;},true);
window.__requests=[];window.__completed=0;window.__lastProposal=null;window.__hold=false;
const originalFetch=window.fetch.bind(window);
window.fetch=async (url,options)=>{
 window.__requests.push(String(url));
 if(window.__hold)await new Promise(resolve=>window.__release=resolve);
 try {const r=await originalFetch(String(url).replace('http://127.0.0.1:8000',location.origin+'/__s05_api'),options);
 if(String(url).endsWith('/api/recommendations')&&r.ok)window.__lastProposal=await r.clone().json();return r;}
 finally{window.__completed++;}
};
""")
            cdp.call('Page.navigate',url='http://127.0.0.1:5190/')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"))
            check('initial_export_disabled','AC-01',js("document.querySelector('.export-button').disabled"))
            def submit():
                target=js('window.__completed')+1
                js("document.querySelector('.planner-form').requestSubmit()")
                wait_for(lambda:js(f"window.__completed>={target} && !document.querySelector('.submit-button').disabled"))
            def download(keyboard=False):
                for p in downloads.glob('*.json'):p.unlink()
                count=js('window.__requests.length')
                entries=js("performance.getEntriesByType('resource').filter(e=>['fetch','xmlhttprequest','beacon'].includes(e.initiatorType)).length")
                cdp.call('Page.bringToFront')
                js("document.querySelector('.export-button').focus()")
                assert js("document.activeElement===document.querySelector('.export-button')")
                if keyboard:
                    for kind in ('keyDown','keyUp'):cdp.call('Input.dispatchKeyEvent',type=kind,key='Enter',code='Enter',windowsVirtualKeyCode=13,nativeVirtualKeyCode=13,text='\r' if kind=='keyDown' else '')
                else:cdp.call('Runtime.evaluate',expression="document.querySelector('.export-button').click()",userGesture=True)
                path=wait_for(lambda:next(downloads.glob('*.json'),None));data=json.loads(path.read_text(encoding='utf8'))
                time.sleep(.2)
                check('export_no_transport_'+data['origin'],'AC-04',js('window.__requests.length')==count and js("performance.getEntriesByType('resource').filter(e=>['fetch','xmlhttprequest','beacon'].includes(e.initiatorType)).length")==entries)
                return data,path.name
            report['phase']='submit_API'
            submit()
            report['phase']='download_API_keyboard'
            print('API submitted',flush=True)
            api=js('window.__lastProposal');data,name=download(True)
            check('real_download_matches_API','AC-02',all(data[k]==v for k,v in api.items()) and data['format_version']==1 and data['origin']=='api',data)
            check('filename_json_keyboard','AC-04',name=='opita360-itinerario.json',name)
            js("(()=>{const e=document.querySelector('#budget');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,'10000');e.dispatchEvent(new Event('input',{bubbles:true}));})()")
            edited,_=download()
            check('exports_last_proposal_not_edited_form','AC-02',edited==data and js("document.querySelector('#budget').value==='10000'"))
            js("window.__hold=true;document.querySelector('.planner-form').requestSubmit()")
            wait_for(lambda:js("document.querySelector('.submit-button').disabled"))
            check('disabled_during_new_generation','AC-01',js("document.querySelector('.export-button').disabled"))
            js('window.__hold=false;window.__release()');wait_for(lambda:js("!document.querySelector('.submit-button').disabled"))
            tree=cdp.call('Accessibility.getFullAXTree')['nodes']
            check('export_accessible_name','AC-04',any(n.get('role',{}).get('value')=='button' and n.get('name',{}).get('value')=='Descargar itinerario JSON' for n in tree))
            for width in (360,1280):
                cdp.call('Emulation.setDeviceMetricsOverride',width=width,height=900,deviceScaleFactor=1,mobile=False)
                check('export_fits_'+str(width),'AC-04',js("(()=>{const r=document.querySelector('.export-button').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})()"))
            cdp.call('Network.setBlockedURLs',urls=['*__s05_api*'])
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"))
            submit();demo,name=download()
            names=js("[...document.querySelectorAll('.result-details h3')].map(e=>e.textContent)")
            check('demo_explicit_origin_and_visible_destinations','AC-03',demo['origin']=='demo' and [d['name'] for d in demo['itinerary']]==names,demo)
            check('demo_totals_visible','AC-02',js("document.querySelector('.result-total b').textContent")==js("new Intl.NumberFormat('es-CO',{style:'currency',currency:'COP',maximumFractionDigits:0}).format("+str(demo['estimated_total'])+")"))
            check('no_runtime_exceptions','regression',not cdp.exceptions,cdp.exceptions)
        except Exception as exc:
            report['error']={'type':type(exc).__name__,'message':str(exc)}
            report['download_files']=[p.name for p in downloads.iterdir()] if 'downloads' in locals() else []
            if cdp:
                try:report['diagnostic']=js("({focus:document.activeElement?.outerHTML,exportClicks:window.__exportClicks,anchorClicks:window.__anchorClicks,completed:window.__completed,requests:window.__requests,proposal:window.__lastProposal,exportDisabled:document.querySelector('.export-button')?.disabled,error:document.querySelector('[role=alert]')?.textContent,results:document.querySelector('#resultado')?.innerText})")
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
            save(report,'s05-browser')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
