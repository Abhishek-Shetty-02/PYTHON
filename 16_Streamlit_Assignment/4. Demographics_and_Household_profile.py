from Utils.load_data import load_data
import numpy as np
import pandas as pd


df = load_data()

# % Male vs Female
# grouped=df['CODE_GENDER']
# grouped


# Avg Age — Defaulters
# Avg Age — Non-Defaulters


# % With Children = % (CNT_CHILDREN > 0)

# With_Children= CNT_CHILDREN df[CNT_CHILDREN>0]  
# With_Children

# Avg Family Size = mean(CNT_FAM_MEMBERS)

Avg_Family_Size= df['CNT_FAM_MEMBERS'].mean()
Avg_Family_Size


# % Married vs Single (from NAME_FAMILY_STATUS)
# % Higher Education (Bachelor+)

# df['NAME_EDUCATION_TYPE']

# % Living With Parents (NAME_HOUSING_TYPE == 'With parents')
# % Currently Working (derive from occupation/employment)

# Avg Employment Years
data1=df['DAYS_EMPLOYED'] 

EMPLOYMENT_YEARS= -data1/365.25
EMPLOYMENT_YEARS

x=EMPLOYMENT_YEARS
y=len(list(df.columns))

AVG_EMPLOYMENT_YEARS= x/y
AVG_EMPLOYMENT_YEARS