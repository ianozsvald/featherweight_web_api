import json
from functools import partial
from flask import Flask, request
app = Flask(__name__)

try:
    import numpy as np
except NameError:
    pass # if numpy isn't available then the user can't be encoding using it

class NumPyEncoder(json.JSONEncoder):
    def default(self, obj):
        # numpy types aren't JSON-serialisable by default, we have to convert
        # them to Python types
        #if 'np' in dir():
        try:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.str):
                return str(obj)
            if isinstance(obj, np.int_):
                return obj.tolist() # int(obj)
            if isinstance(obj, np.float_):
                return float(obj)
        except NameError:
            pass # if numpy isn't available, we don't need to do any conversions
        return json.JSONEncoder.default(self, obj)

def jsonify_numpy(*args, **kwargs):
    """Specialised version of Flask's jsonify which is numpy-friendly"""
    # original jsonify code:
    #indent = None
    #return app.response_class(json.dumps(dict(*args, **kwargs),
        #indent=indent),
        #mimetype='application/json')

    # encode the input args using our numpy-friendly encoder
    encoded = json.dumps(*args, cls=NumPyEncoder)
    return app.response_class(encoded,
        mimetype='application/json')

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
            try:
                value = float(value)
            except ValueError:
                pass
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
    #return json.dumps({'result': result,
                       #'error_msg': error_msg,
                       #'success': success})
    #return jsonify({'result': result,
                       #'error_msg': error_msg,
                       #'success': success})
    d = {'result': result,
         'error_msg': error_msg,
         'success': success}
    return jsonify_numpy(d)


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
