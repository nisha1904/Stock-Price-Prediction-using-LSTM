# -*- coding: utf-8 -*-
"""stock_price_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12kcfh6Xwd73IM03Pw_JKgMCIbV_whq-c
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout

df=pd.read_csv("ADANIPORTS.csv")
training_data=df.iloc[:,4:5].values
print(training_data)

scale= MinMaxScaler(feature_range=(0,1))
training_data_scaled=scale.fit_transform(training_data)

x_train=[]
y_train=[]
for i in range(60,len(training_data_scaled)):
    x_train.append(training_data_scaled[i-60:i,0])
    y_train.append(training_data_scaled[i,0])
x_train,y_train=np.array(x_train),np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model=Sequential()
model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,epochs=100,batch_size=32)

df_1=pd.read_excel('test_data.xlsx')
test_data=df_1.iloc[:,4:5].values

total_data=pd.concat((df['Open'],df_1['Open']),axis=0)
test_input=total_data[len(total_data)-len(df_1)-60:].values
test_input=test_input.reshape(-1,1)
test_input=scale.transform(test_input)
x_test=[]
for i in range(60,141):
  x_test.append(test_input[i-60:i,0])
x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
predictions=model.predict(x_test)
predictions=scale.inverse_transform(predictions)
print(predictions)

plt.plot(test_data, color = 'red', label = 'Real stock Price')
plt.plot(predictions, color = 'blue', label = 'Predicted Stock Price')
plt.title('ADANIPORTS Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('ADANIPORTS Stock Price')
plt.legend()
plt.show()