import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

df = pd.read_csv('2800.HK (2).csv')
df.shape

df = df.drop(columns=['Date','Adj Close'])

import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

plt.figure(figsize=(12,12))
plt.plot(df['Close'])

scaler = MinMaxScaler(feature_range=(0,1))
df = scaler.fit_transform(df)   #Jadi numpy array, tidak lagi pandas



y_close = df[:,3]


plt.figure(figsize=(12,12))
plt.plot(y_close)
plt.show()

ntrain = int(len(y_close)*(0.5))


train = df[0:ntrain]

test = df[ntrain:len(df)]


y_close_train = y_close[0:ntrain]
y_close_test  = y_close[ntrain:len(y_close)]

import numpy as np


def to_sequences(seq_size, data, close):
    x = []
    y = []

    for i in range(len(data) - seq_size - 1):
        window = data[i:(i + seq_size)]
        after_window: object = close[i + seq_size]
        window = [[x] for x in window]
        x.append(window)
        y.append(after_window)

    return np.array(x), np.array(y)


timesteps = 10

x_train, y_train = to_sequences(timesteps, train, y_close_train)
x_test, y_test = to_sequences(timesteps, test, y_close_test)

print("Shape of x_train: {}".format(x_train.shape))
print("Shape of x_test: {}".format(x_test.shape))
print("Shape of y_train: {}".format(y_train.shape))
print("Shape of y_test: {}".format(y_test.shape))

x_train[0]

x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[2], x_train.shape[1],x_train.shape[3]))
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[2],x_test.shape[1],x_test.shape[3]))

print(x_train.shape)

import numpy as np
import pandas as pd

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from keras.layers import Conv1D, Conv2D, MaxPooling2D
from keras.layers.core import Dense, Activation, Flatten, Dropout
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.preprocessing import MinMaxScaler
import csv
import collections
from scipy.stats import zscore
from datetime import datetime
import matplotlib.pyplot as plt

cnn = Sequential()
cnn.add(Conv2D(8, kernel_size = (1, 2), strides = (1, 1),  padding = 'valid',
               activation = 'relu', input_shape = (1,10,5)))
cnn.add(MaxPooling2D(pool_size = (1,2)))

cnn.add(Flatten())
cnn.add(Dense(64, activation="relu"))
cnn.add(Dropout(0.5))
cnn.add(Dense(1, activation="relu"))
cnn.summary()

cnn.compile(loss='mean_squared_error', optimizer='nadam')

monitor = EarlyStopping(monitor='val_loss', min_delta=1, patience=2, verbose=2, mode='auto')
checkpointer = ModelCheckpoint(filepath="Desktop", verbose=0, save_best_only=True) # save best model

history = cnn.fit(x_train,y_train,validation_split=0.2,batch_size = 128, callbacks=[checkpointer],verbose=1,epochs = 100)

plt.plot(history.history['loss'], label = 'loss')
plt.plot(history.history['val_loss'], label = 'val loss')
plt.legend()

cnn.load_weights('CNN_Parameters.hdf5')
pred = cnn.predict(x_test)

print(pred)

score = np.sqrt(metrics.mean_squared_error(y_test, pred))
print("RMSE Score: {}".format(score))





plt.plot(y_test, label = 'actual')
plt.plot(pred,   label = 'CNN')
plt.legend()
plt.show()
