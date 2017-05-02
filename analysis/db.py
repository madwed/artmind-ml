from psycopg2 import connect

class create_cursor:
  def __enter__(self):
    self.connection = connect("dbname=artmind user=postgres")
    self.cursor = self.connection.cursor()
    return self.cursor

  def __exit__(self, type, value, traceback):
    self.connection.commit()
    self.cursor.close()
    self.connection.close()
