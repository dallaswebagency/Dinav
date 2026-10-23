import glob,re,os,urllib.request,urllib.parse
BASE='https://www.dinav.net/wp-content/uploads/'
pat=re.compile(r'https://www\.dinav\.net/wp-content/uploads/[^"\'\s)<>]+')
files=glob.glob('*.html')
urls=set()
for f in files: urls|=set(pat.findall(open(f,encoding='utf-8').read()))
os.makedirs('assets/img',exist_ok=True)
ok={}
for u in sorted(urls):
    rel=urllib.parse.unquote(u[len(BASE):])
    name=rel.replace('/','-')
    dest='assets/img/'+name
    try:
        if not os.path.exists(dest):
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=40).read()
            open(dest,'wb').write(data)
        ok[u]=dest
    except Exception as e:
        print('FAIL',u,e)
for f in files:
    s=open(f,encoding='utf-8').read()
    for u,d in ok.items(): s=s.replace(u,d)
    open(f,'w',encoding='utf-8').write(s)
print(len(ok),'of',len(urls))
