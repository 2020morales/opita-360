"""Integrated S01-S05 real Chrome/CDP tests, unique reports and owned-process cleanup."""
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
    report={'spec':'integration','started_at':datetime.now(timezone.utc).isoformat(),
            'command':['python','-B','-m','harness.integration_browser'],'source_snapshot':before,'checks':checks,
            'limitations':['Chrome headless/CDP, not human screen-reader or full WCAG audit.',
                'API success uses a test-only same-origin proxy in Vite 5195 to real FastAPI 8000; production API URL and CORS unchanged.',
                'Offline scenario blocks API requests; unknown municipality option is a declared desynchronization fixture; storage denial is injected, not a production failure.']}
    def js(expr): return cdp.js(expr)
    def check(name,ac,condition,observed=None):
        checks.append({'name':name,'acceptance':ac,'passed':bool(condition),'observed':observed});print(name,bool(condition),flush=True)
    with tempfile.TemporaryDirectory(prefix='opita-integration-') as tmp:
        try:
            for port in (8000,5195,9245):
                with socket.socket() as probe:probe.bind(('127.0.0.1',port))
            commands=[([sys.executable,'-B','-m','uvicorn','app.main:app','--app-dir','backend','--port','8000'],ROOT),
                ([shutil.which('npm.cmd'),'run','dev','--','--host','127.0.0.1','--strictPort','--port','5195','--config','tests/integration.vite.config.mjs'],ROOT/'frontend')]
            for i,(cmd,cwd) in enumerate(commands):
                stream=open(Path(tmp)/f'server-{i}.log','w',encoding='utf-8');logs.append(stream)
                processes.append(subprocess.Popen(cmd,cwd=cwd,stdout=stream,stderr=stream,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            wait_for(lambda:get_json('http://127.0.0.1:8000/'))
            wait_for(lambda:urllib.request.urlopen('http://127.0.0.1:5195/',timeout=2).status==200)
            chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
            processes.append(subprocess.Popen([str(chrome),'--headless=new','--remote-debugging-port=9245','--remote-allow-origins=http://localhost',
                '--user-data-dir='+str(Path(tmp)/'chrome'),'--no-first-run','--no-default-browser-check','about:blank'],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            targets=wait_for(lambda:get_json('http://127.0.0.1:9245/json/list'))
            cdp=CDP(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
            report['browser']=get_json('http://127.0.0.1:9245/json/version')['Browser']
            for method in ('Page.enable','Runtime.enable','Network.enable','Accessibility.enable'):cdp.call(method)
            import json, time
            downloads=Path(tmp)/'downloads';downloads.mkdir()
            cdp.call('Browser.setDownloadBehavior',behavior='allow',downloadPath=str(downloads),eventsEnabled=True)
            import json, hashlib
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source="""
window.__requests=[];window.__completed=0;window.__lastProposal=null;
const originalFetch=window.fetch.bind(window);
window.fetch=async(url,options)=>{
 window.__requests.push({url:String(url),body:options?.body?JSON.parse(options.body):null});
 try {const r=await originalFetch(String(url).replace('http://127.0.0.1:8000',location.origin+'/__integration_api'),options);
 if(String(url).endsWith('/api/recommendations')&&r.ok)window.__lastProposal=await r.clone().json();return r;}
 finally{window.__completed++;}
};
""")
            def input_value(selector,value):
                js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,{json.dumps(value)});el.dispatchEvent(new Event('input',{{bubbles:true}}));}})()")
            def select(selector,value):
                js(f"(()=>{{const el=document.querySelector({json.dumps(selector)});el.value={json.dumps(value)};el.dispatchEvent(new Event('change',{{bubbles:true}}));}})()")
            def names():return js("[...document.querySelectorAll('.destination-card h3')].map(e=>e.textContent)")
            def favorite(name):
                js(f"[...document.querySelectorAll('.destination-card')].find(e=>e.querySelector('h3').textContent==={json.dumps(name)}).querySelector('.heart').click()")
            def cost(value):
                input_value('#max-cost',value);js("document.querySelector('.cost-filter').requestSubmit()")
            def submit():
                target=js('window.__completed')+1
                js("document.querySelector('.planner-form').requestSubmit()")
                wait_for(lambda:js(f"window.__completed>={target}&&!document.querySelector('.submit-button').disabled"))
            def key(name,code):
                for kind in ('keyDown','keyUp'):cdp.call('Input.dispatchKeyEvent',type=kind,key=name,code=name,windowsVirtualKeyCode=code,nativeVirtualKeyCode=code)
            def download(origin):
                for p in downloads.glob('*.json'):p.unlink()
                before=js('window.__requests.length')
                cdp.call('Runtime.evaluate',expression="document.querySelector('.export-button').click()",userGesture=True)
                path=wait_for(lambda:next(downloads.glob('*.json'),None));data=json.loads(path.read_text(encoding='utf8'))
                check('download_local_'+origin,'S05',js('window.__requests.length')==before and data['origin']==origin and data['format_version']==1,{'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'json':data})
                return data
            cdp.call('Page.navigate',url='http://127.0.0.1:5195/')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"))
            check('all_controls_present','S01-S05',js("document.querySelectorAll('.detail-open').length===8&&!!document.querySelector('#max-cost')&&!!document.querySelector('#only-favorites')&&!!document.querySelector('#trip-municipality')&&document.querySelector('.export-button').disabled"))
            favorite('Malecón del río Magdalena');favorite('Centro de Neiva y tradición opita')
            js("document.querySelector('#only-favorites').click()")
            select('#municipality-filter','Neiva')
            js("[...document.querySelectorAll('.filters button')].find(e=>e.textContent==='Cultura').click()")
            input_value('input[aria-label="Buscar destinos por nombre o municipio"]','Neiva');cost('35000')
            wait_for(lambda:names()==['Malecón del río Magdalena'])
            check('cost_favorites_municipality_category_search_AND','S02+S03',names()==['Malecón del río Magdalena'],names())
            js("document.querySelector('.detail-open').click()")
            wait_for(lambda:js("document.querySelector('.detail-content')?.textContent.includes('35000')||document.querySelector('.detail-content')?.textContent.includes('35.000')"))
            check('detail_of_filtered_favorite','S01+S02+S03',js("document.querySelector('.destination-detail h2').textContent==='Malecón del río Magdalena'"))
            key('Escape',27);wait_for(lambda:js("!document.querySelector('dialog')"))
            check('detail_close_restores_origin_focus','S01+S03',js("document.activeElement.classList.contains('detail-open')"))
            favorite('Malecón del río Magdalena');wait_for(lambda:len(names())==0)
            check('remove_filtered_favorite_preserves_focus_and_storage','S02+S03',js("document.activeElement.id==='only-favorites'&&JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids.join(',')==='8'"))
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='API conectada'"))
            check('favorites_survive_initialization_after_combined_filters','S03',js("JSON.parse(localStorage.getItem('opita360:favorites:v1')).ids.join(',')==='8'&&document.querySelector('.heart.saved')!==null"))
            select('#municipality-filter','Rivera');cost('0');wait_for(lambda:len(names())==0)
            select('#trip-municipality','Neiva');submit()
            proposal=js('window.__lastProposal');data=download('api')
            check('catalogue_filters_do_not_restrict_planner','S02+S03+S04',len(names())==0 and len(proposal['itinerary'])==2 and all(d['municipality']=='Neiva' for d in proposal['itinerary']))
            check('municipal_proposal_export_equals_real_API','S04+S05',all(data[k]==v for k,v in proposal.items()))
            input_value('#budget','10000');older=download('api')
            check('edited_form_does_not_change_exported_municipal_proposal','S04+S05',older==data)
            input_value('#budget','0');submit();zero=download('api')
            check('zero_budget_exception_survives_export','S04+S05',zero['estimated_total']==35000 and zero['budget']==0 and zero['remaining_budget']==0)
            input_value('#budget','200000')
            js("(()=>{const o=document.createElement('option');o.value='Municipio sin destinos';o.textContent='Fixture: catálogo desincronizado';document.querySelector('#trip-municipality').appendChild(o)})()")
            select('#trip-municipality','Municipio sin destinos');submit();empty=download('api')
            check('empty_municipal_proposal_export','S04+S05',empty['itinerary']==[] and empty['estimated_total']==0 and empty['remaining_budget']==200000 and js("!!document.querySelector('.result-empty')"))
            cdp.call('Network.setBlockedURLs',urls=['*__integration_api*']);cdp.call('Page.reload')
            wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"))
            js("document.querySelector('#only-favorites').click()");cost('35000');select('#trip-municipality','Neiva');submit();demo=download('demo')
            check('demo_recovery_ignores_catalogue_filters_and_stays_local','S02+S03+S04+S05',len(names())==0 and len(demo['itinerary'])==2 and all(d['municipality']=='Neiva' for d in demo['itinerary']))
            js("[...document.querySelectorAll('.cost-filter button')].find(e=>e.type==='button').click()")
            wait_for(lambda:names()==['Centro de Neiva y tradición opita'])
            js("document.querySelector('.detail-open').click()");wait_for(lambda:js("!!document.querySelector('.detail-content')"))
            check('demo_detail_of_persisted_favorite','S01+S03',js("document.querySelector('.destination-detail').textContent.includes('Modo demostración')"))
            key('Escape',27);wait_for(lambda:js("!document.querySelector('dialog')"))
            cdp.call('Page.addScriptToEvaluateOnNewDocument',source="Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied for test','SecurityError')}})")
            cdp.call('Page.reload');wait_for(lambda:js("document.querySelector('.api-pill')?.textContent==='Modo demostración'"))
            favorite('Malecón del río Magdalena');js("document.querySelector('#only-favorites').click()");select('#trip-municipality','Neiva');submit();session=download('demo')
            check('storage_denial_keeps_detail_planner_and_export_usable','S03+S04+S05',names()==['Malecón del río Magdalena'] and js("document.querySelector('.favorites-notice').textContent.includes('Solo esta sesión')") and len(session['itinerary'])==2)
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
            save(report,'integration-browser')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
