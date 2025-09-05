import streamlit as st
import numpy as np
from Utils.load_data import load_data
import pandas as pd
import matplotlib.pyplot as plt

df = load_data()
# pd=df.DataFrame(df)

st.title("📊 Overview Dashboard")

#Preprocessing
st.markdown("Preprocessing the Dataset")

# Convert ages: 
data=df['DAYS_BIRTH']
AGE_YEARS=(-data/ 365.25)
AGE_YEARS

st.subheader("Age years")

# st.line_chart(AGE_YEARS, x="Age years",y="id")

# Create a histogram
plt.hist(data, bins=10,color='skyblue', edgecolor='black')
 
# Display the plot in Streamlit
st.pyplot()


# Employment tenure: 

# EMPLOYMENT_YEARS = DAYS_EMPLOYED / 365.25   #(clip huge positives used as “not employed” codes)
data1=df['DAYS_EMPLOYED'] 

EMPLOYMENT_YEARS= -data1/365.25
EMPLOYMENT_YEARS

# Create ratios:

x=df['AMT_INCOME_TOTAL']
# Create a histogram
plt.hist(x,bins=10,color='purple',edgecolor='black')
 
# Display the plot in Streamlit
st.pyplot()

y=df['AMT_CREDIT']
# Create a histogram
plt.hist(y,bins=10)
 
# Display the plot in Streamlit
st.pyplot()

DTI = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
DTI

LOAN_TO_INCOME = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
LOAN_TO_INCOME

ANNUITY_TO_CREDIT = df['AMT_ANNUITY'] / df['AMT_CREDIT']
ANNUITY_TO_CREDIT


# Handle missing values (report % and apply strategy: drop columns > 60% missing; impute median/most-frequent for others)
# total_orders = df['Order ID'].nunique()


# Standardize categories (merge rare categories under “Other” if share < 1%)




# Outlier handling: Winsorize top/bottom 1% for skewed numeric features used in charts



# Define income brackets (quantiles): Low (Q1), Mid (Q2–Q3), High (Q4)
a=df['AMT_INCOME_TOTAL']
# print(a.max())
# print(a.min())

p25=np.percentile(a,25)
p50=np.percentile(a,50)
p75=np.percentile(a,75)
p100=np.percentile(a,100)
print(p25)
print(p50)
print(p75)
print(p100)

# df['AMT_INCOME_TOTAL'].apply(lambda x: "Low" if x<p25, elif  "Mid" if x>=p50 and x<=p75, else  "High")

# Ensure consistent filters (gender, education, family status, housing, income bracket, age range)

# Global filters
# category_filter1 = st.multiselect("Select Gender", options=df["CODE_GENDER"]), default=df["CODE_GENDER"].unique()

# category_filter2 = st.multiselect("Select Education", options=df["NAME_EDUCATION_TYPE"]), default=df["NAME_EDUCATION_TYPE"].unique()

# category_filter3 = st.multiselect("Select Family Status", options=df["NAME_FAMILY_STATUS"]), default=df["NAME_FAMILY_STATUS"].unique()

# category_filter4 = st.multiselect("Select Housing Type", options=df["NAME_HOUSING_TYPE"]), default=df["NAME_HOUSING_TYPE"].unique()

# Income_bracket_filter = st.slider("Minimum Value", min_value=int(df["AGE_YEARS"].min()), max_value=int(df["AGE_YEARS"].max()), value=int(df["AGE_YEARS"].min()))

# Age_range_filter = st.slider("Minimum Value", min_value=int(df["AGE_YEARS"].min()), max_value=int(df["AGE_YEARS"].max()), value=int(df["AGE_YEARS"].min()))

# date_filter = st.date_input("Select Date Range", value=(df["NAME_FAMILY_STATUS"].min(), df["NAME_FAMILY_STATUS"].max()))

# Filter the dataframe
# filtered_df = df[
#     (df["CODE_GENDER"].isin(category_filter1)) &
#     (df["NAME_EDUCATION_TYPE"].isin(category_filter2)) &
#     (df["NAME_FAMILY_STATUS"].isin(category_filter3)) &
#     (df["NAME_HOUSING_TYPE"].isin(category_filter4))]
    # (df["AGE_YEARS"] >= min_value) &
    # (df["Age_range_filter"].between(date_filter[0], date_filter[1]))
    


# st.write("Filtered Data:")
# st.dataframe(filtered_df)