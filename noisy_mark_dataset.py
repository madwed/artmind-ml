from marks import load as load_marks
import collections
from random import randint
import numpy as np

class DataSet(object):
  def __init__(self, marks):
    noisy = np.array([add_noise(mark[0]) for mark in marks])
    clean = np.array([mark[0] for mark in marks])

    self._noisy = noisy
    self._marks = clean
    self._num_examples = len(noisy)
    self._epochs_completed = 0
    self._index_in_epoch = 0

  def marks(self):
    return self._marks

  def noisy(self):
    return self._noisy

  def next_batch(self, batch_size):
    start = self._index_in_epoch
    self._index_in_epoch += batch_size

    if self._index_in_epoch > self._num_examples:
      self._epochs_completed += 1

      perm = np.arange(self._num_examples)
      np.random.shuffle(perm)
      self._noisy = self._noisy[perm]
      self._marks = self._marks[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size

    end = self._index_in_epoch

    return self._noisy[start:end], self._marks[start:end]

def add_noise(image):
  noisy = [0] * len(image)
  for i, point in enumerate(image):
    # if randint(0, 3) == 1:
      # noisy[i] = abs(image[i] - randint(0, 150))
    # else:
    noisy[i] = image[i]
  return noisy

DataSets = collections.namedtuple('Datasets', ['train', 'validation', 'test'])

def load(validation_size=100, test_size=50):
  marks = load_marks()

  if not 0 <= validation_size <= len(marks):
    raise ValueError(
      'Validation size should be between 0 and {}. Received: {}.'
      .format(len(train_images), validation_size))

  validation_limit = validation_size + test_size
  test_marks = marks[:test_size]
  validation_marks = marks[test_size:validation_limit]
  train_marks = marks[validation_limit:]

  train = DataSet(train_marks)
  validation = DataSet(validation_marks)
  test = DataSet(test_marks)

  return DataSets(train=train, validation=validation, test=test)
