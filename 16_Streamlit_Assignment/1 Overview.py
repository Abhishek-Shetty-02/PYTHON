import streamlit as st
import numpy as np
from Utils.load_data import load_data
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.mstats import winsorize


df = load_data()

# Global filters

df = pd.DataFrame({
    "Gender": ["M", "F","M", "F","M", "F"],
    "Education": ["Secondary", "secondary special", "Higher education","Secondary", "secondary special", "Higher education"],
    "Family Status": ["Single", "not married", "Married", "Civil marriage","Separated","Widow"],
    "Housing": ["House", "apartment", "With parents","House", "apartment", "With parents"],
    "Income": [25650,112500,147150, 202500,1000000,117000000],
    "Age": [11,20,30,37,43,69]
})

# –
 
st.sidebar.title("🔍 Global Filters")

# Gender filter
gender_options = df["Gender"].unique().tolist()
selected_gender = st.sidebar.multiselect("Gender", options=gender_options, default=gender_options)

# Education filter
education_options = df["Education"].unique().tolist()
selected_education = st.sidebar.multiselect("Education", options=education_options, default=education_options)

# Family Status filter
family_options = df["Family Status"].unique().tolist()
selected_family = st.sidebar.multiselect("Family Status", options=family_options, default=family_options)

# Housing filter
housing_options = df["Housing"].unique().tolist()
selected_housing = st.sidebar.multiselect("Housing", options=housing_options, default=housing_options)

# Income Bracket filter
income_options = df["Income"].unique().tolist()
selected_income = st.sidebar.multiselect("Income Bracket", options=income_options, default=income_options)

# Age Range filter
age_min = int(df["Age"].min())
age_max = int(df["Age"].max())
selected_age_range = st.sidebar.slider("Age Range", min_value=age_min, max_value=age_max,
                                       value=(age_min, age_max), step=1)

# Apply filters to the dataset
filtered_df = df[
    df["Gender"].isin(selected_gender) &
    df["Education"].isin(selected_education) &
    df["Family Status"].isin(selected_family) &
    df["Housing"].isin(selected_housing) &
    df["Income"].isin(selected_income) &
    df["Age"].between(selected_age_range[0], selected_age_range[1])
]

# Main content
st.title("📊 Dashboard with Global Filters")
st.write("Filtered Data Preview:")
st.dataframe(filtered_df)

# pd=df.DataFrame(df)

# st.title("📊 Overview Dashboard")

#Preprocessing
# st.markdown("Preprocessing the Dataset")

# Convert ages: 
# data=df['DAYS_BIRTH']
# AGE_YEARS=(-data/ 365.25)
# AGE_YEARS

# st.subheader("Age years")

# st.line_chart(AGE_YEARS, x="Age years",y="id")

# Create a histogram
# plt.hist(data, bins=10,color='skyblue', edgecolor='black')
 
# Display the plot in Streamlit
# st.pyplot()


# Employment tenure: 

# EMPLOYMENT_YEARS = DAYS_EMPLOYED / 365.25   #(clip huge positives used as “not employed” codes)
# data1=df['DAYS_EMPLOYED'] 

# EMPLOYMENT_YEARS= -data1/365.25
# EMPLOYMENT_YEARS

# Create ratios:

# x=df['AMT_INCOME_TOTAL']
# # Create a histogram
# plt.hist(x,bins=10,color='purple',edgecolor='black')
 
# # Display the plot in Streamlit
# st.pyplot()

# y=df['AMT_CREDIT']
# # Create a histogram
# plt.hist(y,bins=10)
 
# # Display the plot in Streamlit
# st.pyplot()

# DTI = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
# DTI

# LOAN_TO_INCOME = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
# LOAN_TO_INCOME

# ANNUITY_TO_CREDIT = df['AMT_ANNUITY'] / df['AMT_CREDIT']
# ANNUITY_TO_CREDIT

# Feature Engineering 

# Convert age in years
# df["AGE_YEARS"] = (-df["DAYS_BIRTH"]) / 365.25

if 'DAYS_BIRTH' in df.columns:
    df["AGE_YEARS"] = (-df["DAYS_BIRTH"]) / 365.25
else:
    print("Column 'DAYS_BIRTH' not found in DataFrame.")

# Convert employment duration
# Clip huge positives (e.g., 365243) as "not employed" placeholders
df["DAYS_EMPLOYED_CLEAN"] = df["DAYS_EMPLOYED"].replace({365243: np.nan})
df["EMPLOYMENT_YEARS"] = (-df["DAYS_EMPLOYED_CLEAN"]) / 365.25

# Debt-to-income ratio
df["DTI"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]

# Loan to income ratio
df["LOAN_TO_INCOME"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]

# Annuity to credit ratio
df["ANNUITY_TO_CREDIT"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]

### -----------------------------
### 2. Handle Missing Values
### -----------------------------

missing_report = df.isnull().mean().sort_values(ascending=False) * 100
print("🔍 Missing Value Report (%):\n", missing_report[missing_report > 0])

# Drop columns with >60% missing
to_drop = missing_report[missing_report > 60].index.tolist()
df.drop(columns=to_drop, inplace=True)

# Impute remaining: numeric -> median, categorical -> mode
for col in df.columns:
    if df[col].isnull().any():
        if df[col].dtype in ["float64", "int64"]:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

### -----------------------------
### 3. Standardize Rare Categories
### -----------------------------

def merge_rare_categories(col, threshold=0.01):
    freq = df[col].value_counts(normalize=True)
    rare = freq[freq < threshold].index
    df[col] = df[col].replace(rare, 'Other')

# Apply to object (categorical) columns
for col in df.select_dtypes(include=["object"]).columns:
    merge_rare_categories(col)

### -----------------------------
### 4. Outlier Handling (Winsorization)
### -----------------------------

# Columns to winsorize
winsor_cols = ["AGE_YEARS", "EMPLOYMENT_YEARS", "DTI", "LOAN_TO_INCOME", "ANNUITY_TO_CREDIT"]

for col in winsor_cols:
    df[col] = winsorize(df[col], limits=[0.01, 0.01])

### -----------------------------
### 5. Define Income Brackets (Quantiles)
### -----------------------------

q1 = df["AMT_INCOME_TOTAL"].quantile(0.25)
q3 = df["AMT_INCOME_TOTAL"].quantile(0.75)

def income_bracket(x):
    if x <= q1:
        return "Low"
    elif x <= q3:
        return "Mid"
    else:
        return "High"

df["INCOME_BRACKET"] = df["AMT_INCOME_TOTAL"].apply(income_bracket)

st.title("📊 Insurance Dashboard Metrics")

# --- Basic Metrics ---
st.subheader("📌 Summary Metrics")
st.metric("Average Age (Years)", round(df["AGE_YEARS"].mean(), 1))
st.metric("Median DTI", round(df["DTI"].median(), 3))
st.metric("Avg Employment Years", round(df["EMPLOYMENT_YEARS"].mean(), 1))

# --- Plot 1: Age Distribution ---
fig1, ax1 = plt.subplots()
ax1.hist(df["AGE_YEARS"], bins=10, color='skyblue', edgecolor='black')
ax1.set_title("Age Distribution")
ax1.set_xlabel("Age (Years)")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# --- Plot 2: Employment Years ---
fig2, ax2 = plt.subplots()
ax2.hist(df["EMPLOYMENT_YEARS"], bins=10, color='orange', edgecolor='black')
ax2.set_title("Employment Duration Distribution")
ax2.set_xlabel("Years Employed")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# --- Plot 3: Debt-to-Income Ratio ---
fig3, ax3 = plt.subplots()
ax3.hist(df["DTI"], bins=10, color='purple', edgecolor='black')
ax3.set_title("Debt-to-Income (DTI) Ratio")
ax3.set_xlabel("DTI")
ax3.set_ylabel("Count")
st.pyplot(fig3)

# --- Plot 4: Income Bracket Distribution ---
fig4, ax4 = plt.subplots()
df["INCOME_BRACKET"].value_counts().plot(kind='bar', color='green', edgecolor='black', ax=ax4)
ax4.set_title("Income Brackets")
ax4.set_xlabel("Bracket")
ax4.set_ylabel("Count")
st.pyplot(fig4)









# Handle missing values (report % and apply strategy: drop columns > 60% missing; impute median/most-frequent for others)
# total_orders = df['Order ID'].nunique()


# Standardize categories (merge rare categories under “Other” if share < 1%)




# Outlier handling: Winsorize top/bottom 1% for skewed numeric features used in charts



# Define income brackets (quantiles): Low (Q1), Mid (Q2–Q3), High (Q4)
# a=df['AMT_INCOME_TOTAL']
# print(a.max())
# print(a.min())

# p25=np.percentile(a,25)
# p50=np.percentile(a,50)
# p75=np.percentile(a,75)
# p100=np.percentile(a,100)
# print(p25)
# print(p50)
# print(p75)
# print(p100)

# df['AMT_INCOME_TOTAL'].apply(lambda x: "Low" if x<p25, elif  "Mid" if x>=p50 and x<=p75, else  "High")

# Ensure consistent filters (gender, education, family status, housing, income bracket, age range)
