HTTP API for run-bhyve

Create test VM:

```
curl http://10.0.0.2:8080/create/ubuntu
{
  "host": "test", 
  "image": "ubuntu"
}
```

Destroy test VM:


`curl http://10.0.0.2:8080/destroy`
