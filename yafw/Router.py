__author__ = 'longwei'


import sys

def load_controller(string):
  module_name, function_name = string.split(':', 1)
  __import__(module_name)
  module = sys.modules[module_name]
  func = getattr(module, function_name)
  return func



#loading test
func = load_controller('App:echo')
print func("hello world")
