#!/usr/bin/python

import time,urllib,urllib2,cookielib,getpass,HTMLParser 
import shelve,re,hashlib,os,pynotify,syslog,keyring 
import os

pwd = os.popen("echo -n $PWD").read()
syslog.openlog("Courses")
syslog.syslog(syslog.LOG_ALERT,"courses.py started")

def authenticate(param): 
	jar=cookielib.CookieJar() 
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(jar)) 
	user_agent = 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0' 
	opener.addheaders=[('User-Agent' , user_agent)] 
	urllib2.install_opener(opener) 
	data=None 
	request=urllib2.Request('https://login.iiit.ac.in/cas/login?service=http%3A%2F%2Fcourses.iiit.ac.in%2FEdgeNet%2Fhome.php',data) 
	try:
		response=urllib2.urlopen(request) 
	except:
		if '!@#$%^' not in param :
			print 'Please Check Your Internet Connection'
			os.remove('./data')
		exit() 
	html=response.read() 
	class MyParser(HTMLParser.HTMLParser): 
		def handle_starttag(self,tag,attrs): 
			if tag=='form': 
				for k,v in attrs: 
					if k=='action': 
						self.action=v 
						break 
			elif tag=='input': 
				self.flag=0 
				for k,v in attrs: 
					if k=='name' and v=='lt': 
						self.flag=1 
					if k=='value' and self.flag==1: 
						self.lt=v 
						break 
	parse=MyParser() 
	parse.feed(html) 
	action=parse.action 
	lt=parse.lt 
	if '!@#$%^' not in param :
		user=raw_input('Username [eg- fname.lname@students.iiit.ac.in] : ')
		pwd=getpass.getpass()
		keyring.set_password('Courses',user,pwd)
		param['!@#$%^']=user
	else :
		pwd=keyring.get_password('Courses',param['!@#$%^']) 	
	values={'username':param['!@#$%^'], 'password':pwd, 'lt':lt, '_eventId':'submit'} 
	action='https://login.iiit.ac.in'+action 	
	data=urllib.urlencode(values) 
	request=urllib2.Request(action,data) 	
	response=urllib2.urlopen(request)
	return 0

def hash_foo(page,course_id):
	request=urllib2.Request('http://courses.iiit.ac.in/EdgeNet/'+page+'?select='+course_id)
	try:
		response=urllib2.urlopen(request)
	except:
		return -1
	out=hashlib.md5()
	st=response.read()
	match=re.search(r'<table cellspacing = "?8"?.*?</table>',st)
	out.update(match.group(0))
	return out.digest()
	

class Head(urllib2.Request):
	def get_method(self):
		return "HEAD"

def test(url,dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        f=shelve.open(dir+'.datasync',writeback=True)
        data=urllib2.urlopen(url).read()
        match=re.findall(r'(<tr><td><font color = "#585858"><font.*?</tr>)',data)
        for j in match:
            l=hashlib.md5(j).digest()
	    down=re.findall(r'<a href="(.*?)"',j)
	    if  down:
	    	if(down[0].startswith('/EdgeNet/')):
	   	 	req=urllib2.urlopen(Head('http://courses.iiit.ac.in'+down[0]))
			filename=re.findall(r'filename="(.*?)"',str(req.info()))[0]
                	if not (f.has_key(filename) and f[filename]==l) :
			    req=urllib2.urlopen('http://courses.iiit.ac.in'+down[0])
			    f2=open(dir+filename,'w')
			    f2.write(req.read())
			    f2.close()
        	            f[filename]=l
        f.close()


def check(hash_list,course_id,dir):
        test('http://courses.iiit.ac.in/EdgeNet/resources.php?select=%s' %(course_id),dir+hash_list[0]+'/Resources/')
        test('http://courses.iiit.ac.in/EdgeNet/assignments.php?select=%s' %(course_id),dir+hash_list[0]+'/Assignments/')
	p=pynotify.init("11")
	ret=hash_foo('resources.php',course_id)
	if ret != hash_list[1] and ret != -1:
                test('http://courses.iiit.ac.in/EdgeNet/resources.php?select=%s' %(course_id),dir+hash_list[0]+'/Resources/')
		hash_list[1]=ret
		p=pynotify.Notification(hash_list[0],"Resources Updated!  http://courses.iiit.ac.in/",pwd+"iiith_logo.gif")
		p.show()
	ret=hash_foo('assignments.php',course_id)
	if ret != hash_list[2] and ret !=-1:
                test('http://courses.iiit.ac.in/EdgeNet/assignments.php?select=%s' %(course_id),dir+hash_list[0]+'/Assignments/')
		hash_list[2]=ret
		p=pynotify.Notification(hash_list[0],"Assignments Updated!  http://courses.iiit.ac.in/",pwd+"iiith_logo.gif")
		p.show()
	ret=hash_foo('allthreads.php',course_id)
	if ret != hash_list[3] and ret !=-1:
		hash_list[3]=ret
		p=pynotify.Notification(hash_list[0],"Threads Updated!  http://courses.iiit.ac.in/",pwd+"iiith_logo.gif")
		p.show()


def start_notify(data):
        dir=raw_input('Enter absolute path of Saving-Directory (must start and end with a \'/\' ) : ')
        data['dir']=dir
	li=['resources.php','assignments.php','allthreads.php']
	request=urllib2.Request('http://courses.iiit.ac.in/EdgeNet/home.php')
	try:
		response=urllib2.urlopen(request)
	except:
		print "Check Your Internet Connection and Try Again"
		data.close()
		os.remove('./data')
		exit()
	st=response.read()	
	mat=re.findall(r'coursecheck.php\?select=(.*?) "',st)
	match=re.findall(r'<font color="#0000CC" size="2">(.*?)</font>',st)
	for i in range(len(mat)):
		course_id=mat[i]
		course_name=match[i]
		data[course_id]=[course_name]
		for i in li:
			data[course_id].append(hash_foo(i,course_id))


if 'data' not in os.listdir(pwd):
	data=shelve.open(pwd+'/data',writeback=True)
	p=authenticate(data)
	start_notify(data)
else:
	data=shelve.open(pwd+'/data',writeback=True)
	p=authenticate(data)



for i in data:
	if i != '!@#$%^' and i !='dir'and i != '100':
		check(data[i],i,data['dir'])

data.close()
syslog.openlog("Courses")
syslog.syslog(syslog.LOG_ALERT,"courses.py ended")
			
