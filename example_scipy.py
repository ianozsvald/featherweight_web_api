import numpy as np
import featherweight_api
from scipy import optimize

def f(x):
    return x**2 + 10*np.sin(x)

def function(b, c):
    return optimize.fminbound(f, b, c)

# If called with arguments:
# http://127.0.0.1:5000/function?b=2&c=10
# we get a correct output:
# {"success": true, "error_msg": null, "result": 3.83746830432337}

if __name__ == "__main__":
    featherweight_api.register(function)
    featherweight_api.run()
