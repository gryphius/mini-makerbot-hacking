Running network services
------------------------

 - 80  : http server
 - 443 : https server
 - 9999: json-rpc server

Extracting the Firmware
-----------------------

 - get the firmware from http://192.168.23.44/firmware/firmware.zip
 - unzip -> contains rootfs (ubifs image)
 - install https://github.com/jrspruitt/ubi_reader and https://github.com/jd-boyd/python-lzo
 - `extract_files.py rootfs` -> rootfs will be extracted to output folder
 
Interesting Files
-----------------
 - `/usr/lib/python3.3/site-packages/kaiten/*` -> this is the python stuff controlling everything
 - `/usr/lib/python3.3/site-packages/bwcamera.py` -> camera access/image decoding
 - `/usr/local/apatche/cgi-bin/fcgi_server.py` -> the fcgi server code handling /auth and /camera requests
 - `/etc/httpd.conf` -> apache configuration


Fcgi Server Oauth
-----------------

we claim to be MakerWare, the client_secret can be anything

```
  http://192.168.23.44/auth?response_type=code&client_id=MakerWare&client_secret=secret
```
  
result:

```
  {"client_id": "MakerWare", "username": "Anonymous", "status": "ok", "answer_code": "<ANSCODE>"}
```

request authorisation:

```
  http://192.168.23.44/auth?response_type=answer&client_id=MakerWare&answer_code=<ANSCODE>&client_secret=secret
```


as long as we are not authorized, we will get:

```
  {"answer": "pending", "username": "Anonymous"}
```

The button on the makerbot should be flashing, press it once to authorize the client. Afer that the answer from the above url will be

```
  {"code": "<AUTHCODE>", "username": "Anonymous", "answer": "accepted"}
```

now we can request a token:

```
  http://192.168.23.44/auth?response_type=token&client_id=MakerWare&context=camera&client_secret=secret&auth_code=<AUTHCODE>
```

result:

```
  {"status": "success", "username": "Anonymous", "access_token": "<ACCESSTOKEN>"}
```

and finally we can request the camera data:

```
  192.168.23.44/camera?token=<ACCESSTOKEN>
```

**TODO**: we get a file at this point, but it looks like the camera hasn't been initialized yet, so we don't get a real image :(


JSON-RPC server
---------------

methods:

```
    def ping(self, username:str) -> bool:
    def authenticate(self, access_token:str, client=None) -> None:
    def sync_account_to_bot(self, client=None) -> None:
    def expire_thingiverse_credentials(self, client=None) -> None:
    def set_thingiverse_credentials(self, thingiverse_username:str, thingiverse_token:str, client=None) -> None:
    def register_token(self, access_token:str, username:str, thingiverse_token:str) -> bool:
    def register_lcd(self, client) -> bool:
    def register_client_name(self, client, name) -> bool:
    def register_fcgi(self, client) -> bool:
    def lcd_authorize_user(self, username:str, callback=None) -> None:
    def get_system_information(self, username:str) -> dict:
    def capture_image(self, username:str, output_file:str, callback=None) -> None:
    def transfer_progress(self, local_path:str, progress:int,
    def add_transfer_callback(self, local_path, callback):
    def birdwing_list(self, username:str, path:str) -> list:
```


example call (telnet 192.168.23.44 9999):

send: 

```
  {"params": {"username": "conveyor", "host_version": "PUT_A_REAL_VERSION_HERE"}, "jsonrpc": "2.0", "method": "handshake", "id": 0}
```

result:
```
{"result": {"machine_type": "tinkerbell", "pid": 4, "machine_name": "MakerBot Replicator Mini", "iserial": "<serial>", "commit": "30199ba", "vid": 9153, "port": "9999", "builder": "Release_Birdwing_1.0", "ip": null, "firmware_version": {"minor": 1, "build": 100, "major": 1, "bugfix": 0}}, "jsonrpc": "2.0", "id": 0}
```

Image decoding
--------------

- TODO: the bot seems to use 'libyuv2jpg.so' to decode the image - https://code.google.com/p/libyuv/
 - alternative: try to access save_jpeg over jsonrpc and then pull the image from http server?




