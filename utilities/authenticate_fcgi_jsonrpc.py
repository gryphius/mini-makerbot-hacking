#!/usr/bin/python
import json
import socket
import urllib2
import time


host='192.168.23.44'
jsonrpcport=9999
client_secret='secret'
client_id='MakerWare'

def jsonrpc(method,params):
  d={
    "jsonrpc": "2.0",
    "method": method,
    "id": 0,
    "params": params,
   }
  enc=json.dumps(d)
  return enc

def download(url):
  response=urllib2.urlopen(url)
  return response.read()

def call_fcgi(method,params):
  querystring=""
  for k,v in params.iteritems():
    querystring+="&%s=%s"%(k,v)
  querystring=querystring[1:]
  
  
  url="http://%s/%s?%s"%(host,method,querystring)
  print ""
  print "fcgi request : %s"%url
  result=download(url)
  print "fcgi response: %s"%result
  print ""
  return json.loads(result)
  
def call_jsonrpc(method,params):
  jsoncontent=jsonrpc(method,params)
  print ""
  print "jsonrpc request :%s"%jsoncontent
  rpcsocket.sendall(jsoncontent)
  rcv=rpcsocket.recv(1024)
  print "jsonrpc response: %s"%rcv
  print ""
  return rcv

def request_token(auth_code,context):
  assert context in ['put','camera','jsonrpc']
  result=call_fcgi('auth',dict(response_type='token',client_id=client_id,client_secret=client_secret,context=context,auth_code=auth_code))
  assert result['status']=='success',"Request token failed: %s"%result['status']
  return result['access_token']


if __name__=='__main__':

  AUTH_CODE=None 
  
  #put AUTH_CODE here to skip authentication step
  #AUTH_CODE="CTkNHoyrASpaMJfccOwQIzRuvpHhNpbB"
  
  rpcsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  rpcsocket.connect((host,jsonrpcport),)
  
  
  print "connected to jsonrpc server"
  
  call_jsonrpc("handshake",dict(username="conveyor", host_version="PUT_A_REAL_VERSION_HERE"))
  
  if AUTH_CODE==None:
    print "STARTING AUTHENTICATION...."
    
    fcgi_auth_result=call_fcgi('auth',dict(response_type='code',client_id=client_id,client_secret=client_secret))
    
    assert 'answer_code' in fcgi_auth_result,"Did not get answer_code"
    
    answer_code=fcgi_auth_result['answer_code']
    
    print "GOT ANSWER CODE: %s"%answer_code
    
    while True:
      result=call_fcgi('auth',dict(response_type='answer',client_id=client_id,client_secret=client_secret,answer_code=answer_code))
      assert 'answer' in result
      if result['answer']=='pending':
        print "PRESS THE BUTTON ON THE MAKERBOT TO CONFIRM AUTHORISATION"
        time.sleep(3)
        continue
      elif result['answer']=='accepted':
        break
      else:
        print "unknown answer code: %s"%result['answer']

    AUTH_CODE=result['code']
    
  print "AUTH CODE : %s"%AUTH_CODE
  
  token=request_token(AUTH_CODE,'jsonrpc')
  
  print "Got auth token: %s"%token
  
  #now authenticate in jsonrpc
  call_jsonrpc("authenticate",dict(access_token=token))
 
  #now we should be able to call privileged methods
  #actually works.. but can't see the picture - what would the correct path be?
  #call_jsonrpc("capture_image",dict(username="conveyor", output_file="/home/logs/test.jpg"))
  



  
  

   
    
  