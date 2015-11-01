# featherweight_web_api
Featherweight web API provider for serving R&amp;D methods as web functions

Goals:
* Make it easy to experiment with R&D code by serving it as a web-based API
* Specification-less function registration
* Provision of useful error messages at run-time to diagnose issues

Example:

```
import featherweight_api

def myfn(x, c):
    """Example function"""
    result = x*x + c
    return result

featherweight_api.register(myfn)  # register our function
featherweight_api.run()  # run the server on localhost:5000
```

If you put the following into your browser to make a GET request

```
http://localhost:5000/myfn?x=2&c=10
```

then you'll get the correct output:

```
{"success": true, "result": 14.0, "error_msg": null}
```

# If called without arguments using:
# http://localhost:5000/myfn
# then we get a useful error message
# {"result": null, "error_msg": "TypeError(\"myfn() missing 2 required positional arguments: 'x' and 'c'\",)", "success": false}

