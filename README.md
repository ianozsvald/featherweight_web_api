# featherweight_web_api
Featherweight web API provider for serving R&amp;D methods as web functions

Goals:
* Make it easy to experiment with R&D code by serving it as a web-based API
* Specification-less function registration
* Provision of useful error messages at run-time to diagnose issues
* Automatic conversion of text arguments to floats by default (can be disabled during registration)

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

If you call this without the right arguments such as:

```
http://localhost:5000/myfn
```

then we get a useful error message:
```
{"result": null, "error_msg": "TypeError(\"myfn() missing 2 required positional arguments: 'x' and 'c'\",)", "success": false}
```

If your code raises an exception (e.g. see this in `example.py`):
```
http://localhost:5000/my_badly_written_function
```
then you'll get a helpful debug message:
```
{"result": null, "success": false, "error_msg": "ZeroDivisionError('division by zero',)"}
```


