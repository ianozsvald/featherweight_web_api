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


def extract_parameters(data, auto_convert_arguments, request_is_a_get):
    """
    Extract the parameters present on data. Data is a Dict with the parameters
    received on the request

    :param data: Dictionary with the data
    :param auto_convert_arguments: If True, the parameters will be converted to float
    :return: A dictionary with the data
    """
    d = {}
    if request_is_a_get:
        # GET requests are all-text, so we *might* need to convert them
        # and their value is always a list of items, we only ever want the
        # first item
        for k, v in data.items():
            value = v[0]
            if auto_convert_arguments:
                try:
                    value = float(value)
                except ValueError:
                    pass
            d[k] = value
    else:
        # POST requests are encoded as text, ints or whatever, so we
        # don't need to decode and we always get a key-value pair
        for k, v in data.items():
            value = v
            d[k] = value
    return d


def wrapper(fn, auto_convert_arguments):
    """This gets called when user invokes the API

    :param fn: the function we'll call when invoked
    :param auto_convert_arguments: if True will use `float(arg)` on each input argument"""

    result = {
        'success': True,
        'error_msg': None,
        'result': None
    }

    request_is_a_get = True

    if request.method == 'GET':
        # extract 1st item (as x=1&x=2&x=3 would generates a list of 3 x values)
        # and build new kwarg dictionary
        request_parameters = dict(request.args)
    elif request.method == 'POST':
        jsn = request.get_json()
        assert jsn is not None, "The JSON decode is None, did you pass in good JSON and the application/json mimetype?"
        request_parameters = dict(jsn)
        auto_convert_arguments = None
        request_is_a_get = False
    else:
        result['success'] = False
        result['error_msg'] = 'Invalid method: "{}"'.format(request.method)
        return result

    # call function
    try:
        params = extract_parameters(request_parameters, auto_convert_arguments, request_is_a_get)
        fn_result = fn(**params)
    except Exception as err:
        result['success'] = False
        result['error_msg'] = repr(err)
        fn_result = None

    result['result'] = fn_result

    return jsonify_numpy(result)


def register(fn, auto_convert_arguments=True):
    """Register a function

    fn - the function we'll call when invoked
    auto_convert_arguments - if True will use `float(arg)` on each input argument"""
    # get its name, make a url
    fn_name = fn.__name__
    url = "/{}".format(fn_name)
    # create a partial function
    fn_wrapped = partial(wrapper, fn=fn, auto_convert_arguments=auto_convert_arguments)
    app.add_url_rule(url, fn_name, fn_wrapped, methods=['GET', 'POST'])


def run(host=None, port=None, debug=True):
    """Start the Flask server with our registered functions"""
    app.run(host=host, port=port, debug=debug)
