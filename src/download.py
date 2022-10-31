#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sqlite3
import os

#Create a connection to database
con=sqlite3.connect(os.path.realpath('.\\Data\\attrition.db'))

df = pd.read_sql_query("SELECT * FROM attrition", con)
df.to_csv('database.csv',index=False)

