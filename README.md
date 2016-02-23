# Featherweight function-to-Internet-callable-function server
Expose Python functions (or class methods) as a web-enabled function for others to call


> "I used your featherweight_api in order to deploy a phishing classifier as a prototype REST service. By using your API I definitely reduced the time to market a lot." - _Alejandro Correa Bahnsen, Lead Data Scientist at Easy Solutions, Colombia (Feb 2016)_

Goals:
* Data scientist focused tool to publish simple APIs
* It is a "featherweight" server which turns your R&D code into a web-enabled function
* Solve the "but how can we quickly plumb our new-data-sci-code into the demo environment so it shows value to the bosses?" problem without writing a "proper server" (especially if you don't know how to write a Proper Server)
* Publishes a function using Flask with just 3 lines and little web knowledge
* Supports `scikit-learn` and `numpy` objects (without making you think about correct `JSON` encoding) 
* Useful error messages are provided at run-time to help diagnose issues
* Text arguments from an HTTP call are automatically converted to `float` arguments by default

It does *not solve* these problems:
* It is not scalable (it isn't designed for production use)
* It has no security
* It does not replace Flask, Django or any other Proper Web Framework

Written for:
* Python 3.4+ 
* Flask 0.10+

##Example (`example_tiny_function.py`):

Let's make a Python function that calculates something with a couple of input arguments (`myfn`) and then expose it as a web-callable function (`http://localhost:5000/myfn?<args>`). Once you've called it the result is passed back as a JSON block:

```
import featherweight_api

def myfn(x, c):
    """Example function"""
    return = x*x + c

featherweight_api.register(myfn) 
featherweight_api.run()  # run the server on localhost:5000
```

If you put the following into the URL bar in your browser it'll make a GET request and you'll get a successful result:

```
http://localhost:5000/myfn?x=2&c=10
->
{"result": 14.0,
 "success": true, 
 "error_msg": null
}
```

You can also make this call at the command line:
```
$ curl "http://localhost:5000/myfn?x=2&c=10"
{
  "result": 14.0,
  "success": true,
  "error_msg": null
}
```

`requests` makes calling this sort of API quite trivial!
```
In [1]: import requests
In [2]: result = requests.get("http://localhost:5000/myfn?x=2&c=10")
In [3]: result.json()
Out[3]: {'error_msg': None, 'result': 14.0, 'success': True}
```

We can use `curl` to send a `POST` request:
```
curl -H "Content-Type: application/json" -X POST --data '{"x":2,"c":10}' http://localhost:5000/myfn
->
{
  "result": 14,
  "success": true,
  "error_msg": null
}
```

If you call this without the right arguments then you'll get a useful error message:

```
http://localhost:5000/myfn
->
{
 "result": null,
 "success": false,
 "error_msg": "TypeError(\"myfn() missing 2 required 
                           positional arguments: 'x' and 'c'\",)"
}
```

If your code raises an exception then you'll get a useful error message, here for example we can provide a bad argument:
```
http://localhost:5000/myfn?x=2&c=somemistake
->
{"result": null, 
 "success": false,
 "error_msg": "TypeError(\"unsupported operand type(s) for +: 'float' and 'str'\",)", 
}
```


##Scikit-learn example (`example_iris.py`):

You can use this to wrap up more complex code including classes. Here we'll build a class that makes a `scikit-learn` Iris classifier and then serves up a `score` function which a user can call. If they call it with the 4 arguments (2 lengths and 2 widths) then a classification is made by `scikit-learn` and the resulting `numpy` objects are converted to JSON and passed back.

```
http://localhost:5000/score?sepal_length=5.9&sepal_width=3&petal_length=5.1&petal_width=1.8
->
{
    "result": 
    {
        "guessed_class": 2,
        "guessed_label": "virginica"
    },
    "success": true,
    "error_msg": null
}
```

##Scipy example (`example_scipy.py`):

Shows a call to `optimize.fmbound` (thanks Peadar!).

#Notes

By default the `register` function has `auto_convert_arguments=True` whereby each argument that's passed into the call is converted from a string into a `float` (if possible).

You can change the serving details by passing in a different `host=` or `port=`. For example to serve on your public IP you could use `host="0.0.0.0", port=8080` and then if you use your web-facing IP address (e.g. using `ifconfig` to find this) then a visit to something like `http://192.168.0.12:8080/myfn?x=2&c=10` can be made by other machines on your network.

Some Python modules aren't encoded by default by the `JSON` module including `numpy` objects. I've added an encoder which tries to do sensible things.

In Firefox you'll probably want to add the http://jsonview.com/ pretty-printer for a nicer output.

#Further steps

* https://github.com/cenobites/flask-jsonrpc - JSON RPC
* https://github.com/jmcarp/flask-apispec - Flask, JSON, Swagger using input-arg parsing and output marshalling
* https://github.com/timothycrosley/hug - Falcon based RESTful framework
* https://flask-restful-cn.readthedocs.org/en/latest - Flask based RESTful framework
* http://python-eve.org/ if you want to build stronger APIs, uses Flask, SQLAlchemy or MongoDB, provides default entry points and lots more

#Possible additions

* Python 3.5's type annotations could be used to sanity check the input (without you having to declare anything web-centric)
* Exposed docstrings as Swagger (but probably the more complex tools above offer this for free?)
* Decorator support to avoid the registration (?)
* The current tests are very light, these need to be extended to cover more cases and data types

#Thanks

This API was inspired by chats with [Willem Ligtenberg](https://twitter.com/wligtenberg) who presented http://www.openanalytics.eu/r-service-bus at [BudapestBI2015](https://budapestbi2015.sched.org/event/5b80622ad628092c9c7c72ab964a9ba2#.Vjx-x5cU5yQ).

#Discussion

* https://www.reddit.com/r/Python/comments/3snlwz/featherweight_functiontointernetcallablefunction/
