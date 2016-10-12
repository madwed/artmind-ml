from PIL import Image
from functools import reduce

def as_string(path):
  png = Image.open(path) 
  pixels = list(png.getdata())
  return ':'.join(map(__stringify, pixels))

def __stringify(pixel):
  return '' if __is_red(pixel) else str(pixel[0])

def __is_red(pixel):
  return pixel[0] > 225 and pixel[1] < 30 and pixel[2] < 30

if __name__ == '__main__':
  import sys
  print(as_string(sys.argv[1]))
