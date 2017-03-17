from data_and_analysis.db import create_cursor
import numpy as np

def load():
  with create_cursor() as cursor:
    cursor.execute("""
      SELECT image, file_number, file_sub_number, session, width, height, noisy
      FROM padded_marks
    """)

    marks = cursor.fetchall()

    for i, mark in enumerate(marks):
      marks[i] = (expand_image(mark),) + mark[1:]

    return marks

def expand_image(mark):
  image = mark[0]
  width = mark[4]
  height = mark[5]
  return np.array(list(map(__to_int, image.split(':'))))

def __to_int(value):
  return -1 if value == '' else int(value)
