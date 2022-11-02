# -*- coding: utf-8 -*-
"""Linear regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HEJ_lx6_Pk4Hsy_dJH4WWaFEvccYFH_W
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/gdrive')

from google.colab import files
uploaded=files.upload()

df=pd.read_csv('Chennai_house_univariate_train.csv')

df.head()

df.head().plot(kind='bar',x='Size',y='Price')

data= (df-df.mean())/(df.max()-df.min())
data.head(3)

cols=data.shape[1]
print(cols)

rows=data.shape[0]
print(rows)

x=data.iloc[:,0:rows-1]
x.head(3)

y=data.iloc[:,cols-1:cols]
y.head(3)

theta=np.matrix([0,0])
x=np.matrix(x)
y=np.matrix(y)

x.shape,y.shape,theta.shape

def computeError(x,y,theta):
  inner=np.power(((x*theta.T)-y),2)
  return np.sum(inner)/(2*len(x))

computeError(x,y,theta)



learn_rate= 1
iters= 350
def gradientDescent(x,y,theta,learn_rate,iters):
  temp=np.matrix(np.zeros(theta.shape))
  parameters= theta.shape[1]
  cost=[]
  for i in range(iters):
    error=(x*theta.T)-y
    for j in range(parameters):
      gradient= np.multiply(error,x[:,j])
      temp[0,j]=theta[0,j]-((learn_rate/len(x))*np.sum(gradient))
    theta=temp
    cost_iter=computeError(x,y,theta)
    cost.append(cost_iter)
  return theta,cost
new_theta,cost=gradientDescent(x,y,theta,learn_rate,iters)
new_theta
cost

model_price=x*new_theta.T
fig,ax= plt.subplots(figsize=(10,5))
ax.plot(data.Size,model_price,'r',label='Final Model')
ax.scatter(data.Size,data.Price,label='Training data')
ax.legend()
ax.set_xlabel('Size')
ax.set_ylabel('Price')
ax.set_title('Final model Vs Training data')

from sklearn.metrics import mean_absolute_error
Error=mean_absolute_error(model_price,y)
Accuracy=1-Error
print('Error ={}%'.format((round(Error*100,2))))
print('Accuracy={}%'.format((round(Accuracy*100,2))))

def predict (new_theta,accuracy):
  size=float(input("enter the size of house in sqt: "))
  size=(size-df.Size.mean())/(df.Size.max()-df.Size.min())
  price=(new_theta[0,0]+(new_theta[0,1]*size))
  Predicted_Price=(price*(df.Price.max()-df.Price.min()))+(df.Price.mean())
  Price_at_Max_Accuracy=(Predicted_Price*(1/accuracy))
  Price_range=Price_at_Max_Accuracy-Predicted_Price
  return Predicted_Price,Price_range
Predicted_Price, Price_range= predict(new_theta,Accuracy)
print('Your house cost is '+str(round(Predicted_Price*(1/100000),2))+' Lakhs (+ or -) '+str(round(Price_range,2)))
