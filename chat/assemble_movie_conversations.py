import re

def combine():
  lines = str(open('movie_lines.txt', mode='r+b').read())[2:].split('\\n')

  lines_hash = {}
  for line in lines:
    line = line.split(' +++$+++ ')
    lines_hash[line[0]] = re.sub('\\\\', '', line[-1])

  def fill_line(line):
    indices = re.sub('\'', '', re.split('\[', line)[1][0:-1]).split(', ')
    return list(map(lambda i: lines_hash[i], indices))

  conversation_indices = open('movie_conversations.txt').read().split('\n')
  conversation_indices = list(map(fill_line, conversation_indices))

  return conversation_indices

if __name__ == "__main__":
  import sys
  print(combine())
