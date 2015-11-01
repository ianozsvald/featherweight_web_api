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

If you put the following into your browser to make a GET request you'll get a successful result:

```
http://localhost:5000/myfn?x=2&c=10
->
{"success": true, "result": 14.0, "error_msg": null}
```

If you call this without the right arguments then you'll get a useful error message:

```
http://localhost:5000/myfn
->
{"result": null, "error_msg": "TypeError(\"myfn() missing 2 required positional arguments: 'x' and 'c'\",)", "success": false}
```

If your code raises an exception (e.g. see this in `example.py`) then you'll get the error message:
```
http://localhost:5000/my_badly_written_function
->
{"result": null, "success": false, "error_msg": "ZeroDivisionError('division by zero',)"}
```

By default the `register` function has `auto_convert_arguments=True` whereby each argument that's passed into the call is converted from a string into a `float` (if possible).

You can change the serving details by passing in a different `host=` or `port=`. For example to serve on your public IP you could use `host="0.0.0.0", port=8080` and then if you use your web-facing IP address (e.g. using `ifconfig` to find this) then a visit to something like `http://192.168.0.12:8080/myfn?x=2&c=10` can be made by other machines on your network.
