from Utils.load_data import load_data
import numpy as np
import pandas as pd
import streamlit as st

# Global filters

df = pd.DataFrame({
    "Gender": ["M", "F","M", "F","M", "F"],
    "Education": ["Secondary", "secondary special", "Higher education","Secondary", "secondary special", "Higher education"],
    "Family Status": ["Single", "not married", "Married", "Civil marriage","Separated","Widow"],
    "Housing": ["House", "apartment", "With parents","House", "apartment", "With parents"],
    "Income": [25650,112500,147150, 202500,1000000,117000000],
    "Age": [11,20,30,37,43,70]
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


# # Total Applicants = count(SK_ID_CURR)

# Total_Applicants= df['SK_ID_CURR'].count()
# # Total_Applicants

# st.write(f"The Total applicants in the Home Credit: {Total_Applicants}")

# # Default Rate (%) = mean(TARGET) × 100

# Default_Rate= df['TARGET'].mean() * 100

# st.write(f"The Default Rate of the clients in the Home Credit: {Default_Rate}")

# # Repaid Rate (%) = (1 - mean(TARGET)) × 100

# Repaid_Rate = (1-df['TARGET'].mean()) * 100

# st.write(f"The Repaid Rate of the clients in the Home Credit: {Repaid_Rate}")

# # Total Features = number of columns
# a=list(df.columns)
# Total_Features = len(a)

# st.write(f"The Total Features in the Home Credit dataset: {Total_Features}")

# # Avg Missing per Feature (%) = mean(isnull(col)) × 100 averaged over columns

# # # Numerical Features
# # # Categorical Features

# # Median Age (Years) = median(AGE_YEARS)
# data=df['DAYS_BIRTH']
# AGE_YEARS=(-data/ 365.25)
# AGE_YEARS

# Median_Age= AGE_YEARS.median()
# Median_Age

# # Median Annual Income
# Median_Annual_Income= df['AMT_INCOME_TOTAL'].median()
# Median_Annual_Income

# # Average Credit Amount

# x=df['AMT_CREDIT'].sum()
# y=len(list(df.columns))

# Average_Credit_Amount=x/y

# st.write(f"The Average Credit Amount of the clients in the Home Credit dataset: {Average_Credit_Amount}")


# --- Summary Metrics ---

# Total Applicants
total_applicants = df["SK_ID_CURR"].nunique() if "SK_ID_CURR" in df.columns else df.shape[0]

# Default Rate (%)
default_rate = df["TARGET"].mean() * 100 if "TARGET" in df.columns else np.nan

# Repaid Rate (%)
repaid_rate = 100 - default_rate if not np.isnan(default_rate) else np.nan

# Total Features
total_features = df.shape[1]

# Average Missing per Feature (%)
avg_missing_per_feature = df.isnull().mean().mean() * 100

# Feature Type Counts
numerical_features = df.select_dtypes(include=["number"]).shape[1]
categorical_features = df.select_dtypes(include=["object", "category"]).shape[1]

# Median Age (Years)
median_age = df["AGE_YEARS"].median() if "AGE_YEARS" in df.columns else np.nan

# Median Annual Income
median_income = df["AMT_INCOME_TOTAL"].median() if "AMT_INCOME_TOTAL" in df.columns else np.nan

# Average Credit Amount
avg_credit_amt = df["AMT_CREDIT"].mean() if "AMT_CREDIT" in df.columns else np.nan

# --- Display Metrics in Streamlit ---

st.header("📊 Key Applicant Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Applicants", f"{total_applicants:,}")
col2.metric("Default Rate (%)", f"{default_rate:.2f}")
col3.metric("Repaid Rate (%)", f"{repaid_rate:.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Total Features", total_features)
col5.metric("Avg Missing per Feature (%)", f"{avg_missing_per_feature:.2f}")
col6.metric("Numerical / Categorical", f"{numerical_features} / {categorical_features}")

col7, col8, col9 = st.columns(3)
col7.metric("Median Age (Years)", f"{median_age:.1f}")
col8.metric("Median Annual Income", f"${median_income:,.0f}")
col9.metric("Avg Credit Amount", f"${avg_credit_amt:,.0f}")
