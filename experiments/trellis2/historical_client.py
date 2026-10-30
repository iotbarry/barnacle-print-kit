from pathlib import Path
import requests,json,uuid
P=Path(__file__).parent
U='https://microsoft-trellis-2.hf.space/gradio_api'
S=requests.Session();sid=uuid.uuid4().hex
def call(fn,data):
 r=S.post(U+'/queue/join',json=dict(data=data,fn_index=fn,session_hash=sid),timeout=40);r.raise_for_status();print('queued',fn,r.text,flush=True)
 with S.get(U+'/queue/data',params={'session_hash':sid},stream=True,timeout=300) as stream:
  for line in stream.iter_lines():
   if not line.startswith(b'data:'):continue
   msg=json.loads(line[5:]);kind=msg.get('msg')
   if kind=='process_completed':
    out=msg.get('output',{});(P/f'response_{fn}.json').write_text(json.dumps(msg,ensure_ascii=False),encoding='utf-8')
    if not msg.get('success'):raise RuntimeError(str(out)[:1500])
    print('completed',fn,flush=True);return out.get('data')
   if kind in ['queue_full','unexpected_error']:raise RuntimeError(str(msg))
   if kind=='estimation':print('queue rank',msg.get('rank'),flush=True)
call(2,[])
with (P/'单颗参考.png').open('rb') as f:
 r=S.post(U+'/upload',files={'files':('barnacle.png',f,'image/png')},timeout=90);r.raise_for_status();path=r.json()[0]
print('uploaded reference',flush=True)
img={'path':path,'meta':{'_type':'gradio.FileData'}}
prep=call(4,[img])[0]
call(7,[prep,281028,'1024',7.5,.7,12,5.,7.5,.5,12,3.,1.,0.,12,3.])
out=call(9,[None,300000,2048])
for item in out:
 if isinstance(item,dict) and item.get('url'):
  data=S.get(item['url'],timeout=120);data.raise_for_status();(P/'AI生成原始模型.glb').write_bytes(data.content);print('GLB saved',len(data.content),flush=True);break
