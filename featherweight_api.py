import json
from functools import partial
from flask import Flask, request
app = Flask(__name__)


def wrapper(fn, auto_convert_arguments):
    """This gets called when user invokes the API

    fn - the function we'll call when invoked
    auto_convert_arguments - if True will use `float(arg)` on each input argument"""
    d = {}
    # extract 1st item (as x=1&x=2&x=3 would generates a list of 3 x values)
    # and build new kwarg dictionary
    for k, v in dict(request.args).items():
        value = v[0]
        if auto_convert_arguments:
            value = float(value)
        d[k] = value
    # call function
    success = True
    error_msg = None
    result = None
    try:
        result = fn(**d)
    except Exception as err:
        error_msg = repr(err)
        success = False
    return json.dumps({'result': result,
                       'error_msg': error_msg,
                       'success': success})


def register(fn, auto_convert_arguments=True):
    """Register a function

    fn - the function we'll call when invoked
    auto_convert_arguments - if True will use `float(arg)` on each input argument"""
    # get its name, make a url
    fn_name = fn.__name__
    url = "/{}".format(fn_name)
    # create a partial function
    fn_wrapped = partial(wrapper, fn=fn, auto_convert_arguments=auto_convert_arguments)
    app.add_url_rule(url, fn_name, fn_wrapped)


def run(host=None, port=None, debug=True):
    """Start the Flask server with our registered functions"""
    app.run(host=host, port=port, debug=debug)
