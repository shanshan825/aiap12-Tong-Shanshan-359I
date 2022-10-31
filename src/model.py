#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
df=pd.read_csv('processed-data.csv')
df.info()

# ## Step 1. Train_Test_Split
X=df.drop('Attrition',axis=1)
y=df['Attrition']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

from sklearn.metrics import classification_report


# ## Step 2. Train models 

# ### 2.1 Logistic Model

from sklearn.linear_model import LogisticRegression

logr = LogisticRegression()
logr.fit(X_res,y_res)
logr_prediction=logr.predict(X_test)

print(classification_report(y_test,logr_prediction))

# ### 2.2 Random Forest Model

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=600)
rfc.fit(X_res,y_res)
rfc_predictions = rfc.predict(X_test)
print(classification_report(y_test,rfc_predictions))

# #### Fine tune the model using Grid Search

from sklearn.model_selection import GridSearchCV
param_grid=[
    {
        'n_estimators': [200,400,600,800],
        'max_features':[4,6,8,10]
    }
]
gs_rfc=RandomForestClassifier()


grid_search=GridSearchCV(gs_rfc, param_grid, cv=5,scoring='f1_micro',return_train_score=True)
grid_search.fit(X_res,y_res)
grid_search.best_params_

final_model=grid_search.best_estimator_
final_prediction=final_model.predict(X_test)
print(classification_report(y_test,final_prediction))

# ### 2.3 LightGBM Model

import lightgbm as lgb
clf = lgb.LGBMClassifier()
clf.fit(X_train, y_train)
lgb_predictions=clf.predict(X_test)
print(classification_report(y_test,lgb_predictions))


# ### 2.4 SGDClassifier Model

from sklearn.linear_model import SGDClassifier
sgd_clf=SGDClassifier(random_state=42)
sgd_clf.fit(X_train,y_train)
sgd_predictions=clf.predict(X_test)
print(classification_report(y_test,sgd_predictions))





