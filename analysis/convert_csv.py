import pandas as pd
from db import create_cursor

def to_psql(file_path):
  marks = pd.read_csv(file_path) 
  folder = int(folder_name(file_path))
  with create_cursor() as cursor:
    for _, row in marks.iterrows():
      name = row.fileName.replace('.jpg', '').split('_')

      cursor.execute("""
        INSERT INTO marks
        (width, height, image, top, "right", bottom, "left", 
          file_number, file_sub_number, session)
        VALUES
        ({width}, {height}, '{image}', {top}, {right}, {bottom}, {left}, 
          {file_number}, {file_sub_number}, {session});
      """.format(
        width=int(row.imageWidth), 
        height=int(row.imageHeight), 
        image=row.image,
        top=int(row.markTop), 
        right=int(row.markRight), 
        bottom=int(row.markBottom),
        left=int(row.markLeft), 
        file_number=int(name[0]), 
        file_sub_number=int(name[1]), 
        session=folder
      ))

def folder_name(file_path):
  file_name = file_path.rsplit('/', 1)[1]
  return file_name.split('_', 1)[0]

if __name__ == '__main__':
  import sys
  print(to_psql(sys.argv[1]))
