# Client-server protocol for metrics
My realization simple client-server protocol for send metrics
# Client.py
Client have a two method
- put <key> <value> <timestamp>\n --- success answer will be *ok\n\n*, or error *error\nwrong command\n\n*
- get <key>\n --- success answer will be *ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n*
- get * --- answer will be all available metrics

# Server.py
Reply for client requests

# Text example

```
$: telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
< 
```

# TODO
More documentation needed
