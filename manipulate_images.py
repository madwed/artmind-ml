from analysis.db import create_cursor
from math import ceil, floor
import pandas as pd
import numpy as np

def pad(size):
  with create_cursor() as cursor:
    cursor.execute("""
      SELECT 
        image, file_number, file_sub_number, session,
        marks.right - marks.left, 
        marks.bottom - marks.top
      FROM marks 
      WHERE marks.right - marks.left <= {size}
      AND marks.bottom - marks.top <= {size}
    """.format(size=size))
    marks = cursor.fetchall()

    columns = ['image', 'file', 'sub_file', 'session', 'width', 'height']

    for i, mark in enumerate(marks):
      marks[i] = (pad_mark(mark, size),) + mark[1:4] + (size, size)
      cursor.execute("""
        INSERT INTO padded_marks
          (image, file_number, file_sub_number, session, width, height)
        VALUES ('{0}', {1}, {2}, {3}, {4}, {5})
      """.format(*marks[i]))

    marks = pd.DataFrame(data=marks, columns=columns)

    return marks

def pad_mark(mark, size):
  mark_array = np.ndarray(
    shape=(mark[4], mark[5]), 
    dtype=np.int16,
    offset=np.int_().itemsize,
    buffer=np.array(list(map(__to_int, mark[0].split(':'))))
  )
  w_pad = (size - mark[4]) / 2
  h_pad = (size - mark[5]) / 2
  padding = ((ceil(w_pad), floor(w_pad)), (ceil(h_pad), floor(h_pad)))

  padded_mark = np.pad(mark_array, padding, 'constant', constant_values=-1)
  return ':'.join(map(__to_str, padded_mark.flatten().tolist()))

def __to_int(value):
  return -1 if value == '' else int(value)

def __to_str(value):
  return '' if value == -1 else str(value)

if __name__ == '__main__':
  import sys
  print(pad(100))
