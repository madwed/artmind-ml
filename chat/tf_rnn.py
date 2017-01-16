import tensorflow as tf

# Placeholder for the inputs in a given iteration.
words = tf.placeholder(tf.int32, [batch_size, num_steps])

lstm = rnn_cell.BasicLSTMCell(lstm_size)
# Initial state of the LSTM memory.
initial_state = state = tf.zeros([batch_size, lstm.state_size])
probabilities = []
loss = 0.0

for current_batch_of_words in words_in_dataset:
  # The value of state is updated after processing each batch of words.
  output, state = lstm(current_batch_of_words, state)

  # The LSTM output can be used to make next word predictions
  logits = tf.matmul(output, softmax_w) + softmax_b
  probabilities.append(tf.nn.softmax(logits))
  loss += loss_function(probabilities, target_words)

final_state = state
