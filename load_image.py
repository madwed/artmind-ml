from PIL import Image
from functools import reduce
import json

def as_string(path):
  png = Image.open(path) 
  pixels = list(png.getdata())
  return ':'.join(map(__stringify, pixels))

def get_metadata(path, columns):
  metadata = json.load(open(path.replace('jpg', 'json')))
  return list(map(lambda key: metadata[key], columns))

def __stringify(pixel):
  return '' if __is_red(pixel) else str(pixel[0])

def __is_red(pixel):
  return pixel[0] > 225 and pixel[1] < 30 and pixel[2] < 30

