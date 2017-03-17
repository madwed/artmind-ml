import noisy_mark_dataset
import tensorflow as tf
from datetime import datetime
import os
import numpy as np

SIZE = 100 * 100

def main():
  # Load Data
  start = datetime.now()
  print('Loading Data')

  marks = noisy_mark_dataset.load(validation_size=0)

  elapsed = datetime.now() - start
  print('Data Loaded in {} seconds'.format(elapsed.seconds))

  # Set Up Network
  x = tf.placeholder(tf.float32, [None, SIZE])
  W = tf.Variable(tf.zeros([SIZE, SIZE]), name='W')
  b = tf.Variable(tf.zeros([SIZE]), name='b')
  y = tf.matmul(x, W) + b

  y_ = tf.placeholder(tf.float32, [None, SIZE])

  cross_entropy = tf.reduce_mean(
    tf.contrib.losses.mean_squared_error(labels=y_, predictions=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()

  # Train
  start = datetime.now()
  print('Training')

  epochs = 500
  saver = tf.train.Saver([W, b])
  for _ in range(epochs):
    batch_xs, batch_ys = marks.train.next_batch(50)
    sess.run(train_step, feed_dict={ x: batch_xs, y_: batch_ys })

    if _ % 50 == 0:
      saver.save(sess, 'models/noise-reduction', global_step=_)
      elapsed = datetime.now() - start
      print('{} seconds have passed'.format(elapsed.seconds))
      print(sess.run(
        cross_entropy, feed_dict={ x: marks.test.noisy(), y_: marks.test.marks() }))

  elapsed = datetime.now() - start
  print('Trained network in {} seconds'.format(elapsed.seconds))

  # Test trained model
  print(sess.run(
    cross_entropy, feed_dict={ x: marks.test.noisy(), y_: marks.test.marks() }))

def testing():
  marks = noisy_mark_dataset.load(validation_size=0)

  x = tf.placeholder(tf.float32, [None, SIZE])
  W = tf.Variable(tf.zeros([SIZE, SIZE]), name='W')
  b = tf.Variable(tf.zeros([SIZE]), name='b')
  y = tf.matmul(x, W) + b

  y_ = tf.placeholder(tf.float32, [None, SIZE])

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()

  saver = tf.train.Saver([W, b])
  saver.restore(sess, os.getcwd() + '/models/noise-reduction-150')

  ex = sess.run(y, feed_dict={ x: marks.test.noisy() })

  ex = ex[0]
  pos = 0
  neg = 0
  mx = 0
  mn = 10000000000000000000000
  for point in ex:
    if point > 0:
      pos += 1
      if point > mx:
        mx = point
      if point < mn:
        mn = point
    else:
      neg += 1
    print(point)

  print(mx, mn)

if __name__ == '__main__':
  print(testing())
