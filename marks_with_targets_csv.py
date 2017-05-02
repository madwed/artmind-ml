from marks import load
import pandas as pd
import numpy as np

def to_csv():
  return table().to_csv('marks_with_targets.csv')

def table():
  marks = load()
  rows = (row(marks[i], marks[i + 1]) for i in range(0, len(marks) - 1))
  return pd.DataFrame(rows, columns=header(marks))

def header(marks):
  source_pixels = ['source_{}'.format(i) for i in range(len(marks[0][0]))]
  target_pixels = ['target_{}'.format(i) for i in range(len(marks[0][0]))]
  return source_pixels + target_pixels

def row(mark_a, mark_b):
  row_values = np.concatenate((mark_a[0], mark_b[0]))
  return row_values

if __name__ == '__main__':
  import sys
  print(to_csv())
