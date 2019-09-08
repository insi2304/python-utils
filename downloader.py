from requests import Session
import re
import os
import sys

def get_filename(cd):
    if not cd:
        return None
    fname = re.findall('filename="(.+)"', cd)
    if len(fname) == 0:
        return None
    return fname[0]

proxy = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

s = Session() 
if len(sys.argv) < 3:
    print "Usage:",sys.argv[0],"username password"
    exit(1) 
	
username = sys.argv[1]
password = sys.argv[2]
	
s.post("http://52.23.185.72/65bd6d4a-0150-4ecd-98f3-7482692f7872/login.php", {"username":username, "password":password}, proxies=proxy)

if os.path.exists(os.path.join(os.getcwd(),username)):
    print "Cleaning up files under folder:",os.path.join(os.getcwd(),username) 
    os.system("rm -rf "+username)
    print "Cleanup done \n\n"
	
os.mkdir(username)

for i in xrange(1,100):
    for j in ['bug','doc']:
        resp = s.get("http://52.23.185.72/65bd6d4a-0150-4ecd-98f3-7482692f7872/file_download.php?file_id="+str(i)+"&type="+j, allow_redirects=True,proxies=proxy)
        filename = get_filename(resp.headers.get('content-disposition'))
        if filename is not None:
            print "trying to download file:",filename
            open(os.path.join(os.getcwd(),username,filename), 'wb').write(resp.content)
            if os.path.exists(os.path.join(os.getcwd(),username,filename)):
			    print "Successfully downloaded the file:",filename,"\n"
        else:
            continue



