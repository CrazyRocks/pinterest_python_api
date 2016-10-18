import requests
import json
import sys
import time
import hmac
import hashlib
import urllib

base='https://api.pinterest.com/v3/'

key='7c429a941844d5330c6949e62f37519f03b6c275'

head={'X-Pixel-Ratio':'2',
'X-Pinterest-Device':'iPad5,4',
'X-Pinterest-App-Type':'2',
'X-Pinterest-InstallId':'00000000000000000000000000000000',
'X-Pinterest-AppState':'active',
'User-Agent':'Pinterest for iOS/6.12 (iPad; 9.3.3)'}

client_id=1431599

s=requests.session()
s.verify=False
s.headers.update(head)
proxies = {
	'http': 'http://127.0.0.1:8888',
	'https': 'http://127.0.0.1:8888',
}
s.proxies.update(proxies)

def genOauth_signature(url,type='POST'):
	url=urllib.quote_plus(url,safe='&=')
	data='%s&%s'%(type,url)
	return hmac.new(key, data, hashlib.sha256).hexdigest()

def login(user,pasw,client_id,timestamp):
	print '[!] trying login'
	data={'client_id':client_id,
		'password':pasw,
		'timestamp':timestamp,
		'username_or_email':user}
	oauth_signature=genOauth_signature('https://api.pinterest.com/v3/login/&client_id=%s&password=%s&timestamp=%s&username_or_email=%s'%(client_id,pasw,timestamp,user))
	r=s.post(base+'login/?client_id=%s&timestamp=%s&oauth_signature=%s'%(client_id,timestamp,oauth_signature),data=data)
	return json.loads(r.content)
	
def main():
	data= login('my@mail.com','password',client_id,int(time.time()))
	print '[+]server:',data['message'],data['data']['access_token'][:9]+'..'
		
if __name__ == '__main__':
	main()