import os
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd


# load data and post-pad zero's to each sample
X = pd.read_csv(os.path.join('.', 'data', 'after_four_varied.csv'), delimiter=',', header=None, dtype=np.float32,
                names=['a', 'b', 'c', 'd', 'e', 'f', 'g'])
y = pd.read_csv(os.path.join('.', 'data', 'after_four_varied_labels.csv'), header=None).to_numpy()


# split some% of data for training/testing
percent_split = int(len(X.index)*0.7)


# convert X into nested list
list_data = []
for i in range(0, len(X.index)):
    row = []
    for j in range(0, 7):
        if not np.isnan(X.iloc[i, j]):
            row.append(X.iloc[i, j])
    list_data.append(row)


# turn nested list into ragged tensor
list_data = tf.ragged.constant(list_data, dtype=tf.float32)
print(list_data)


# one hot encode labels
enc = OneHotEncoder()
enc.fit(y)
y = enc.transform(y).toarray()
y = tf.convert_to_tensor(y)

print(y[0])
print(y[1])


# split into training & testing
X_train = list_data[0:percent_split][:][:]
y_train = y[0:percent_split]

X_test = list_data[percent_split:][:][:]
y_test = y[percent_split:]

print(X_train.shape[0])
print(X_test.shape[0])


# get max length of input
max_seq = list_data.bounding_shape()[-1]
print("Max Seq = ", max_seq)


# create model
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(None,), dtype=tf.float32, ragged=True),
    tf.keras.layers.Embedding(max_seq, 7),
    tf.keras.layers.SimpleRNN(7),
    tf.keras.layers.Dense(2, activation='sigmoid')
])


# compile model
model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
              optimizer='adam', metrics=['accuracy'])


# fit model with training data
history = model.fit(X_train, y_train, epochs=10)


# layer summary
print(model.summary())


# evaluate model on testing data
test_acc = model.evaluate(X_test, y_test)


# custom tests
print(model.predict(tf.ragged.constant([[2.0, 4.0, 5.0, 4.0]])))
