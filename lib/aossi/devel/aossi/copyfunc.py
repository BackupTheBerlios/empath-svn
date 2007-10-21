from types import FunctionType as function, MethodType as method

def copyfunction(func, name = None, **kwargs):
   isfunc = isinstance(func, function)
   ismeth = isinstance(func, method)
   kwargs_len = len(kwargs)
   if not isfunc and not ismeth:
      raise TypeError, "The first argument must be a python function or method."
   elif name is not None and not isinstance(name, str):
      raise TypeError, "The second argument must be a string or None."
   elif kwargs_len > 1 or (kwargs_len == 1 and kwargs.keys()[0] != 'func_doc'):
      raise TypeError, "'func_doc' is the only allowed keyword argument; got: " + ", ".join(kwargs.keys())
   if name is None or name == "":
      name = func.func_name
   tempfunc = function(func.func_code, func.func_globals, name, func.func_defaults, func.func_closure)
   fdoc = None
   if 'func_doc' in kwargs:
      fdoc = kwargs['func_doc']
   tempfunc.func_doc = fdoc
   return tempfunc
   
##def copymethod(meth, name = None, **kwargs):
##   ismeth = isinstance(meth, method)
##   if not ismeth:
##      raise TypeError, "The first argument must be a python method."
##   elif name is not None and not isinstance(name, str):
##      raise TypeError, "The second argument must be a string or None."
##   if name is None or name == "":
##      name = meth.func_name   
##   tempmeth = copyfunction(meth, name, **kwargs)
##   return method(tempmeth, None)
   
def copymethod(meth, name = None, **kwargs):
   ismeth = isinstance(meth, method)
   if not ismeth:
      raise TypeError, "The first argument must be a python method."
   tempmeth = copyfunction(meth, name, **kwargs)
   return method(tempmeth, None)
