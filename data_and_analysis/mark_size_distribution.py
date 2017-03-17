import matplotlib.pyplot as plt
from db import create_cursor
from operator import itemgetter

def run():
  with create_cursor() as cursor:
    cursor.execute("""
      SELECT 
        marks.right - marks.left as mark_width,
        marks.bottom - marks.top as mark_height
      FROM marks
    """)

    sizes = cursor.fetchall()
    widths = list(map(itemgetter(0), sizes))
    heights = list(map(itemgetter(1), sizes))

    plt.scatter(widths, heights)
    plt.axis([0, 500, 0, 500])
    plt.show()


if __name__ == '__main__':
  import sys
  run()
