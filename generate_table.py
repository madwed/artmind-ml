import load_image
from os import listdir, path
import pandas as pd

keys = ['imageWidth', 'imageHeight', 'markTop', 'markRight', 'markBottom', 'markLeft']

def to_csv(folder):
  return table(folder).to_csv(folder.rsplit('/', 1)[1] + '.csv')

def table(folder):
  jpgs = (doc for doc in listdir(folder) if doc.endswith('.jpg'))
  rows = (row(path.join(folder, jpg)) for jpg in jpgs)
  return pd.DataFrame(rows, columns=header())

def header():
  header_values = keys.copy()
  header_values.append('image')
  header_values.insert(0, 'fileName')
  return header_values

def row(filepath):
  img = load_image.as_string(filepath)
  filename = filepath.rsplit('/', 1)[1]

  row_values = load_image.get_metadata(filepath, keys)
  row_values.append(img)
  row_values.insert(0, filename)
  return row_values

if __name__ == "__main__":
  import sys
  print(to_csv(sys.argv[1]))
