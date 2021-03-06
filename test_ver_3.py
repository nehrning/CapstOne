#!/usr/bin/env python
# coding: utf-8

# In[68]:


import pandas as pd
import numpy as np
import datetime
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.core import Dense, Activation, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import winsound
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

# In[69]:


df = pd.read_csv('dataset.csv')
del df['Unnamed: 0']


# In[70]:


df


# In[73]:


df.columns


# In[74]:


df['name']


# In[75]:


s = df['name']
s


# In[76]:


s = list(set(s))
# print(s)


# In[77]:


len(s)


# In[78]:


def create_dataset(signal_data, look_back=1):
    dataX, dataY = [], []
    for i in range(len(signal_data) - look_back):
        dataX.append(signal_data[i:(i + look_back), 0])
        dataY.append(signal_data[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

look_back = 20


# In[79]:


s[1]


# In[87]:


# for i in range(len(s)):
#     print(s[i] ,':', len(df[df['name']==s[i]]))


# In[88]:


20226480 - 19220360 # 71220 * 284 - rows


# In[89]:


data1 = df[df['name']=='강남(222)']


# In[90]:


data1.columns


# In[91]:


data1


# In[92]:


len(data1)


# In[93]:


data1.shape


# In[ ]:

print(data1)
data = data1['a']
#     data = data.value
data = data.values.astype('float32')
data = data.reshape(len(data), 1)

scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

train_size = int(len(data) * 0.80)
test_size = len(data) - train_size

train = data[0:train_size]
test = data[train_size:len(data)]
x_train, y_train = create_dataset(train, look_back)
x_test, y_test = create_dataset(test, look_back)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
# 모델 구성하기
for i in range(0, 100, 2):
    look_back=i
    model = Sequential()
    model.add(LSTM(512, input_shape=(None, 1), return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(32, input_shape=(None, 1)))
    model.add(Dropout(0.3))
    # model.add(LSTM(i, input_shape=(None, 1)))

    # model.add(Dense(i))
    # model.add(Dropout(0.3))
    # model.add(Dropout(0.3))
    # model.add(Dense(64))

    model.add(Dense(1))
    name = "LSTM512_512_+lookback_"+str(i)+".jpg"
    # 모델 학습과정 설정하기
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
    model.summary()
    hist = model.fit(x_train, y_train, epochs=10, batch_size=16, verbose=2)
    p = model.predict(x_test)


    plt.plot(y_test)
    plt.plot(p)
    plt.legend(['testY', 'p'], loc='upper right')
    plt.title(mean_squared_error(y_test, p))
    # plt.savefig(datetime.datetime.now())
    plt.savefig(name)
    plt.clf()
    print(mean_squared_error(y_test, p))
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

# In[55]:




# In[ ]:




