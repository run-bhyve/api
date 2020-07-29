HTTP API for run-bhyve

Set env vars before starting API:

```
setenv HOST_SERV 10.0.0.1
setenv HOST_USER username
setenv TELETOKEN 123456789:AAWWA_jf2V3L1pNFrbNFrb1zoJ8UM15VIi
setenv ADMIN_TELEGRAM
setenv HOST_API 10.0.0.2
```

## API usage

Create test VM:

```
$ curl http://API_ADDR:8080/create/[debian|centos]/testname

{
  "ip": "10.0.0.12", 
  "name": "testname", 
  "root_pwd": "fffd0c48ea", 
  "user": "linux", 
  "user_pwd": "377ba3a2f8"
}
```

Restart test VM:

```
$ curl http://server:8080/restart/testname

{
  "status": "ok"
}

```

Destroy test VM:

```
$ curl http://server:8080/destroy/testname

{
  "status": "ok"
}

```

