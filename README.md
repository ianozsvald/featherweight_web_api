# Featherweight R&D API Provider
A "featherweight" Flask-based tool to convert your functions into Internet-callable functions

Goals:
* Easily expose a Python function (or class method) as a web-enabled function for others to call
* Publish a function using a Flask-server with just 3 lines
* Useful error messages are provided at run-time to help diagnose issues
* Text arguments are automatically converted to `float` arguments by default

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

#Notes

By default the `register` function has `auto_convert_arguments=True` whereby each argument that's passed into the call is converted from a string into a `float` (if possible).

You can change the serving details by passing in a different `host=` or `port=`. For example to serve on your public IP you could use `host="0.0.0.0", port=8080` and then if you use your web-facing IP address (e.g. using `ifconfig` to find this) then a visit to something like `http://192.168.0.12:8080/myfn?x=2&c=10` can be made by other machines on your network.

Some Python modules aren't encoded by default by the `JSON` module including `numpy` objects. I've added an encoder which tries to do sensible things.

In Firefox you'll probably want to add the http://jsonview.com/ pretty-printer for a nicer output.

#Further steps

You might want to look at https://flask-restful-cn.readthedocs.org/en/0.3.4/ or http://python-eve.org/ if you want to build stronger APIs.
