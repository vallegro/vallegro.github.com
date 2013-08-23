# -*- coding: utf-8 -*- 
import getpass, imaplib, email, re, os, datetime, time, email.charset, base64

def remove_cret(str):
    r=re.compile(r"(.*)\r(.*)",re.DOTALL)
    m=r.match(str)
    while m!=None:
        str=''.join([m.group(1),m.group(2)])
        m=r.match(str)
    return str

def fnu():    
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login('blogvallegro@gmail.com', '123qazWSX')
    M.select()
    typ, data = M.search(None, '(UNSEEN FROM "mao@nii.ac.jp")')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        mailText=data[0][1]
        msg=email.message_from_string(mailText)
        for part in msg.walk():
            if not part.is_multipart():
                contenttype = part.get_content_type()
                tmp=part.as_string()
                r=re.compile(r"(.+Content-Transfer-Encoding: )(.+)(\n\n.+)",re.DOTALL)
                m=r.match(tmp)
                encoding=m.group(2)
                if contenttype in ['text/plain']:
                    charset=part.get_charsets()[0]
                    partcont=part
                    mailContent = part.get_payload()
                    if encoding in ['base64']:
                        mailContent=base64.b64decode(mailContent)
                    if charset in ['gb2312']:
                        charset='gbk'
                    mailContent=mailContent.decode(charset)
                    r=re.compile(r"(.+)name(.+)title(.+)(--.+)",re.DOTALL)
                    m=r.match(mailContent)
                    name = m.group(1)
                    title = m.group(2)
                    title = title[2:len(title)]
                    blograw = m.group(3)
                    blograw = remove_cret(blograw)
                    rakec=''.join(['rake post title=\"',name,'\"'])
                    os.system(rakec)
                    date=datetime.date.today().isoformat()
                    filename=''.join(['./_posts/',date,'-',name,'.md'])
                    newblog=open(filename,'w+b')
                    meta=''.join([u"---\nlayout: post\ntitle: \"",title,u"\"\n---\n{% include JB/setup %}\n"])
                    cont=''.join([meta,blograw])
                    newblog.write(cont.encode("utf-8"))
                    newblog.close()
                    gitc='git add .'
                    os.system(gitc)
                    gitc='git commit -m "email autoupdate"'
                    os.system(gitc)
                    gitc='git push'
                    os.system(gitc)
                    break
    M.close()
    M.logout()

while True:
    try:
        fnu()
    except:
        print 'err'
        time.sleep(120)



