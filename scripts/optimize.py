import glob,os,re,urllib.request
from PIL import Image
D='assets/img/'
BASE='https://www.dinav.net/wp-content/uploads/'
# 1. fetch full-size versions of sized thumbnails
for f in sorted(os.listdir(D)):
    m=re.match(r'^(.*)-(\d+)x(\d+)(\.\w+)$',f)
    if not m: continue
    full=m.group(1)+m.group(4)
    if os.path.exists(D+full) or os.path.exists(D+m.group(1)+'.webp'): continue
    # name is YYYY-MM-name ; rebuild upload path
    y,mo,rest=full.split('-',2)
    url=BASE+y+'/'+mo+'/'+rest
    try:
        data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
        open(D+full,'wb').write(data);print('full',full)
    except Exception as e: print('nofull',full)
# 2. convert everything to webp, max width 1800
renames={}
for f in sorted(os.listdir(D)):
    if not f.lower().endswith(('.png','.jpg','.jpeg')): continue
    p=D+f;w=os.path.splitext(f)[0]+'.webp'
    im=Image.open(p)
    if im.width>1800: im=im.resize((1800,round(im.height*1800/im.width)),Image.LANCZOS)
    if im.mode not in('RGB','RGBA'): im=im.convert('RGBA' if 'transparency' in im.info else 'RGB')
    im.save(D+w,'WEBP',quality=82,method=6)
    os.remove(p);renames[f]=w
for h in glob.glob('*.html'):
    s=open(h,encoding='utf-8').read()
    for a,b in renames.items(): s=s.replace('assets/img/'+a,'assets/img/'+b)
    open(h,'w',encoding='utf-8').write(s)
print(len(renames),'converted')
