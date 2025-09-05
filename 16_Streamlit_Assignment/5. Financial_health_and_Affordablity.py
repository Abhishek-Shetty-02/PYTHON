from Utils.load_data import load_data
import numpy as np
import pandas as pd


df = load_data()


# Avg Annual Income

x=df['AMT_INCOME_TOTAL']
y=len(list(df.columns))

Avg_Annual_Income= x/y

Avg_Annual_Income

# Median Annual Income
x=df['AMT_INCOME_TOTAL'].median()
x
# Avg Credit Amount

x=df['AMT_CREDIT']
y=len(list(df.columns))

Avg_Credit_Amount= x/y

Avg_Credit_Amount

# Avg Annuity

x=df['AMT_ANNUITY']
y=len(list(df.columns))

Avg_Annuity= x/y

Avg_Annuity

# Avg Goods Price

a=df['AMT_GOODS_PRICE']
b=len(list(df.columns))
Avg_Goods_Price= a/b
Avg_Goods_Price

# Avg DTI = mean(AMT_ANNUITY / AMT_INCOME_TOTAL)
DTI = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
DTI

a=DTI
b=len(list(df.columns))
Avg_DTI= a/b
Avg_DTI

# Avg Loan-to-Income (LTI) = mean(AMT_CREDIT / AMT_INCOME_TOTAL)
# Income Gap (Non-def − Def) = mean(income|0) − mean(income|1)
# Credit Gap (Non-def − Def) = mean(credit|0) − mean(credit|1)
# % High Credit (> 1M)
