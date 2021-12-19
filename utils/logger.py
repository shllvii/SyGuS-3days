# set DEBUG a large constant for no debuging information
DEBUG = 2
def log(*value, level=0):
  if level >= DEBUG:
    print(*value)