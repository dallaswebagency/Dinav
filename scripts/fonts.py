import re,urllib.request,os
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
url='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@400..700&family=IBM+Plex+Mono:wght@400;500&display=swap'
css=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA})).read().decode()
os.makedirs('assets/fonts',exist_ok=True)
out=[]
for m in re.finditer(r'/\* ([\w-]+) \*/\s*(@font-face\s*\{.*?\})',css,re.S):
    sub,block=m.group(1),m.group(2)
    if sub not in('latin','latin-ext'): continue
    u=re.search(r'url\((https://[^)]+)\)',block).group(1)
    fam=re.search(r"font-family:\s*'([^']+)'",block).group(1).replace(' ','')
    wt=re.search(r'font-weight:\s*([\d ]+);',block).group(1).replace(' ','-')
    name=f'{fam}-{wt}-{sub}.woff2'
    open('assets/fonts/'+name,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA})).read())
    out.append(block.replace(u,'fonts/'+name))
open('assets/fonts/fonts.css','w').write('\n'.join(out))
print(len(out),'faces')
