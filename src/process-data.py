#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv('database.csv')

# ## Step 1: Correlated columns
# 'Usage Time' is highly correlated to 'Usage Rate';
# Generate a new column 'Hours per Week' to remove correlated columns
df['Hours per Week']=df['Usage Time']*df['Usage Rate']
df.drop(['Usage Time','Usage Rate'],axis=1, inplace=True)

# ## Step 2: Columns with inconsistent or invalid values:
#  2.1 Convert 'Travel Time' column with inconsistent units
# create a function to convert the 'Travel Time' from string with different units to numerical values in mins 
def cal_travel_time(x):
    if x.split()[1]=='mins':
        return int(float(x.split()[0]))
    else:
        return int(float(x.split()[0])*60)

# Apply the function cal_travel_time to column
df['Travel Time']=df['Travel Time'].apply(lambda x: cal_travel_time(x))

# ### 2.2 Convert 'Qualification' column with inconsistent cateogories
df['Qualification'].value_counts()
# convert Bacheloar's into Bachelor; Convert 'Master's' into 'Master'; Convert "Doctor of Philosophy" to "Ph.D"
df['Qualification']=df['Qualification'].map(
    {'Bachelor':'Bachelor',
     'Master':'Master',
     'Ph.D':'Ph.D',
     'Diploma':'Diploma',
    
    "Bachelor's":'Bachelor',
     "Master's":'Master',
     'Doctor of Philosophy':'Ph.D'})

# ### 2.3 Deal with invalid values in 'Monthly Income' columns
df['Monthly Income'].hist(bins=20)
df['Monthly Income']=abs(df['Monthly Income'])

# ### 2.4 Deal with negative value (-1) in 'Age' and 'Birth Year' column
df['Age']=np.where(df['Age']>0, df['Age'], (2022-df['Birth Year']))
df.drop('Birth Year', axis=1, inplace=True)

# ### 2.5 Remove 'Member Unique ID'
# This column does not hold meanings to Attrition
df.drop('Member Unique ID', axis=1, inplace=True)

#Step 3. Cateogrical data
# ### 3.1 Cateogorical Columns without order: 'Gender', 'Branch', 'Work Domain'

df=pd.get_dummies(df,columns=['Gender','Branch','Work Domain'],drop_first=True)

# ### 3.2 Cateogorical Columns with order: Qualification, Membership
from sklearn.preprocessing import OrdinalEncoder
Qua_cat=['Diploma','Bachelor','Master','Ph.D']
Qua_enc = OrdinalEncoder(categories = [Qua_cat])
df[['Qualification']] = Qua_enc.fit_transform(df[['Qualification']])

Mem_cat=['Normal','Bronze','Silver','Gold']
Mem_enc = OrdinalEncoder(categories = [Mem_cat])
df[['Membership']] = Mem_enc.fit_transform(df[['Membership']])

# ## Step 4. Feature Scaling of numerical columns
from sklearn.preprocessing import StandardScaler
num_attribs=['Age', 'Monthly Income', 'Travel Time', 'Months', 'Hours per Week']
scaler = StandardScaler()
df[num_attribs]=scaler.fit_transform(df[num_attribs])

# ## Step 5. Export the pre-processed data
df.to_csv('processed-data.csv',index=False)

