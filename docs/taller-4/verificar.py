"""Reproducible checks. Run with Python having uvicorn, httpx and websockets installed.
Requires npm dependencies installed, Chrome, and free ports 5174/8000/9228.
Never reuses or stops a service it did not start.
"""
import ast
from contextlib import ExitStack
from importlib.metadata import version
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import traceback
from urllib.request import urlopen
from datetime import datetime, timezone
from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'evidencias'
OUT.mkdir(exist_ok=True)
report = {'timestamp_utc':datetime.now(timezone.utc).isoformat(), 'base':'d81614d',
          'python':sys.version, 'packages':{name:version(name) for name in ['fastapi','uvicorn','websockets']}, 'checks':[], 'commands':[], 'limitations':[
              'Browser automation checks are not a complete accessibility audit or screen-reader test.',
              'Catalog replacement uses an explicit browser fixture; connected API checks use real FastAPI.',
              'Test harness adds origin http://127.0.0.1:5174 to CORS in memory only because port 5173 is occupied; production CORS is unchanged.',
              'External photographs depend on network access; layout checks do not prove their availability.']}
processes=[]
logs=[]
ws=None
connections=ExitStack()
counter=0

def command(args,cwd,name):
    p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    (OUT/(name+'.log')).write_text(p.stdout,encoding='utf-8')
    report['commands'].append({'args':args,'exit_code':p.returncode,'log':name+'.log'})
    if p.returncode: raise RuntimeError(name+' failed')

def check(name,condition,actual=None):
    report['checks'].append({'name':name,'passed':bool(condition),'actual':actual})
    if not condition: raise AssertionError(name+': '+repr(actual))

def call(method,params=None):
    global counter
    counter+=1
    ws.send(json.dumps({'id':counter,'method':method,'params':params or {}}))
    while True:
        result=json.loads(ws.recv(timeout=15))
        if result.get('id')==counter:
            if 'error' in result: raise RuntimeError(result['error'])
            return result.get('result',{})

def js(expression):
    v=call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
    if 'exceptionDetails' in v: raise RuntimeError(v['exceptionDetails'])
    return v.get('result',{}).get('value')

def wait(expression):
    end=time.monotonic()+20
    while time.monotonic()<end:
        if js(expression): return
        time.sleep(.1)
    raise TimeoutError(expression)

def select(value):
    js("(()=>{const e=document.querySelector('#municipality-filter');e.value="+json.dumps(value)+";e.dispatchEvent(new Event('change',{bubbles:true}));})()")
    time.sleep(.15)

def category(value):
    js("[...document.querySelectorAll('.filters button')].find(e=>e.textContent==="+json.dumps(value)+").click()")
    time.sleep(.15)

def search(value):
    js("(()=>{const e=document.querySelector('.searchbox input');Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,"+json.dumps(value)+");e.dispatchEvent(new Event('input',{bubbles:true}));})()")
    time.sleep(.15)

def count(): return js("document.querySelectorAll('.destination-card').length")

def screenshot(name):
    js("document.querySelector('#destinos').scrollIntoView()")
    time.sleep(.3)
    (OUT/name).write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))

def spawn(args,cwd,name):
    f=(OUT/(name+'.log')).open('w',encoding='utf-8'); logs.append(f)
    p=subprocess.Popen(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));processes.append(p)
    return p

def http_wait(url):
    end=time.monotonic()+20
    while time.monotonic()<end:
        try:
            with urlopen(url,timeout=1) as response: return json.load(response)
        except Exception: time.sleep(.2)
    raise TimeoutError(url)

try:
    for port in (5174,8000,9228):
        with socket.socket() as s:
            s.bind(('127.0.0.1',port))
    command([shutil.which('npm.cmd'),'test'],ROOT/'frontend','unit')
    command([shutil.which('npm.cmd'),'run','build'],ROOT/'frontend','build')
    for p in (ROOT/'backend/app').glob('*.py'): ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    check('Backend Python syntax without creating pycache',True)
    spawn([sys.executable,'-B','-c',"from app.main import app; import uvicorn; app.user_middleware[0].kwargs['allow_origins'].append('http://127.0.0.1:5174'); uvicorn.run(app,host='127.0.0.1',port=8000)"],ROOT/'backend','api-server')
    data=http_wait('http://127.0.0.1:8000/api/destinations')
    check('Real GET /api/destinations: 8 destinations with municipality',len(data['destinations'])==8 and all(d.get('municipality') for d in data['destinations']))
    spawn(['node',str(ROOT/'frontend/node_modules/vite/bin/vite.js'),'--host','127.0.0.1','--port','5174','--strictPort'],ROOT/'frontend','vite-server')
    chrome=os.environ.get('CHROME_PATH',r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    profile=tempfile.mkdtemp(prefix='opita-t4-chrome-')
    spawn([chrome,'--headless=new','--disable-gpu','--no-first-run','--remote-debugging-port=9228','--user-data-dir='+profile,'about:blank'],ROOT,'chrome')
    targets=http_wait('http://127.0.0.1:9228/json')
    ws=connections.enter_context(connect(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'),max_size=20*1024*1024))
    report['browser']=call('Browser.getVersion')
    call('Page.enable');call('Network.enable')
    call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1000,'deviceScaleFactor':1,'mobile':False})
    call('Page.navigate',{'url':'http://127.0.0.1:5174'})
    wait("document.querySelector('.api-pill')?.textContent==='API conectada'")
    check('React connected to real API',count()==8,count())
    options=js("[...document.querySelector('#municipality-filter').options].map(o=>o.value)")
    expected=['Todos']+sorted(set(d['municipality'] for d in data['destinations']))
    check('Todos and unique municipalities derived from API',options==expected,options)
    for m in options[1:]:
        select(m); n=sum(d['municipality']==m for d in data['destinations'])
        check('API municipality '+m,count()==n,count())
    select('Neiva');category('Cultura');search(' CENTRO ')
    check('API three filters combined',count()==1,count())
    search('');category('Naturaleza')
    check('Empty combination shows clear message',count()==0 and bool(js("document.querySelector('.empty-state')?.textContent.includes('No encontramos')")))
    category('Todos');select('Todos')
    check('Recovery restores eight destinations',count()==8,count())
    check('Select linked to visible label',js("document.querySelector('#municipality-filter').labels.length>0"))
    js("document.querySelector('#municipality-filter').focus()")
    call('Input.dispatchKeyEvent',{'type':'keyDown','key':'n','code':'KeyN','text':'n'})
    call('Input.dispatchKeyEvent',{'type':'keyUp','key':'n','code':'KeyN'})
    time.sleep(.2)
    check('Native select supports keyboard selection',js("document.querySelector('#municipality-filter').value==='Neiva'"))
    select('Todos');screenshot('escritorio.png')
    call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
    check('Mobile selector fits viewport',js("(()=>{const r=document.querySelector('#municipality-filter').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth})()"))
    screenshot('movil.png')
    call('Network.setBlockedURLs',{'urls':['http://127.0.0.1:8000/*']})
    call('Page.reload',{'ignoreCache':True})
    wait("document.querySelector('.api-pill')?.textContent==='Modo demostraci\u00f3n'")
    for m in options[1:]:
        select(m); n=sum(d['municipality']==m for d in data['destinations'])
        check('Demo municipality '+m,count()==n,count())
    select('Neiva')
    category('Cultura');search('centro');check('Demo three filters',count()==1,count())
    call('Network.setBlockedURLs',{'urls':[]})
    fixture="""const original=window.fetch;window.fetch=(...args)=>String(args[0]).endsWith('/api/destinations')?new Promise(resolve=>window.deliverCatalog=()=>resolve({ok:true,json:async()=>({destinations:[{id:99,name:'Fixture',municipality:'Rivera',category:'Bienestar',price:1,days:1,tags:[],color:'green'}]})})):original(...args);"""
    injection=call('Page.addScriptToEvaluateOnNewDocument',{'source':fixture})
    call('Page.reload',{'ignoreCache':True})
    wait("!!window.deliverCatalog&&!!document.querySelector('#municipality-filter')")
    select('Neiva');js('window.deliverCatalog()')
    wait("document.querySelector('#municipality-filter').value==='Todos'&&document.querySelectorAll('.destination-card').length===1")
    check('Controlled delayed catalog resets invalid selection in React',True)
    call('Page.removeScriptToEvaluateOnNewDocument',{'identifier':injection['identifier']})
    report['status']='passed'
except Exception:
    report['status']='failed';report['error']=traceback.format_exc()
finally:
    connections.close()
    for p in reversed(processes):
        p.terminate()
        try:p.wait(timeout=10)
        except subprocess.TimeoutExpired:p.kill();p.wait()
    for f in logs:f.close()
    report['source_sha256']={str(p.resolve().relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'frontend/src/main.jsx',ROOT/'frontend/src/destination-filters.js',ROOT/'frontend/tests/destination-filters.test.js',ROOT/'docs/plan-filtro-municipio.md',Path(__file__)]}
    (OUT/'resultados.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
sys.exit(0 if report['status']=='passed' else 1)
