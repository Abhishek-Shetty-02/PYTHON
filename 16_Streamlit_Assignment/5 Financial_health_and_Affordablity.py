from Utils.load_data import load_data
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib as plt

df = load_data()


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


# Avg Annual Income

# x=df['AMT_INCOME_TOTAL']
# y=len(list(df.columns))

# Avg_Annual_Income= x/y

# Avg_Annual_Income

# # Median Annual Income
# x=df['AMT_INCOME_TOTAL'].median()
# x
# # Avg Credit Amount

# x=df['AMT_CREDIT']
# y=len(list(df.columns))

# Avg_Credit_Amount= x/y

# Avg_Credit_Amount

# # Avg Annuity

# x=df['AMT_ANNUITY']
# y=len(list(df.columns))

# Avg_Annuity= x/y

# Avg_Annuity

# # Avg Goods Price

# a=df['AMT_GOODS_PRICE']
# b=len(list(df.columns))
# Avg_Goods_Price= a/b
# Avg_Goods_Price

# Avg DTI = mean(AMT_ANNUITY / AMT_INCOME_TOTAL)
# DTI = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
# DTI

# a=DTI
# b=len(list(df.columns))
# Avg_DTI= a/b
# Avg_DTI

# Avg Loan-to-Income (LTI) = mean(AMT_CREDIT / AMT_INCOME_TOTAL)
# Income Gap (Non-def − Def) = mean(income|0) − mean(income|1)
# Credit Gap (Non-def − Def) = mean(credit|0) − mean(credit|1)
# % High Credit (> 1M)

st.set_page_config(page_title="Loan Metrics Dashboard", layout="wide")

st.title("📊 Loan Metrics Dashboard")

# Metrics
avg_income = df['AMT_INCOME_TOTAL'].mean()
median_income = df['AMT_INCOME_TOTAL'].median()
avg_credit = df['AMT_CREDIT'].mean()
avg_annuity = df['AMT_ANNUITY'].mean()
avg_goods_price = df['AMT_GOODS_PRICE'].mean()

avg_dti = (df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']).mean()
avg_lti = (df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']).mean()

income_gap = df[df['TARGET'] == 0]['AMT_INCOME_TOTAL'].mean() - df[df['TARGET'] == 1]['AMT_INCOME_TOTAL'].mean()
credit_gap = df[df['TARGET'] == 0]['AMT_CREDIT'].mean() - df[df['TARGET'] == 1]['AMT_CREDIT'].mean()

pct_high_credit = (df['AMT_CREDIT'] > 1_000_000).mean() * 100

# Display metrics
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg Annual Income", f"${avg_income:,.0f}")
col2.metric("Median Annual Income", f"${median_income:,.0f}")
col3.metric("Avg Credit Amount", f"${avg_credit:,.0f}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Annuity", f"${avg_annuity:,.0f}")
col5.metric("Avg Goods Price", f"${avg_goods_price:,.0f}")
col6.metric("High Credit % (> 1M)", f"{pct_high_credit:.2f}%")

    # Plot: DTI & LTI
st.subheader("📉 Ratios: DTI & LTI")
fig1, ax1 = plt.subplots()
ax1.bar(['Avg DTI', 'Avg LTI'], [avg_dti, avg_lti], color=['skyblue', 'orange'])
ax1.set_ylabel("Ratio")
st.pyplot(fig1)

    # Plot: Gaps
st.subheader("⚖️ Gaps: Non-defaulters vs Defaulters")
fig2, ax2 = plt.subplots()
ax2.bar(['Income Gap', 'Credit Gap'], [income_gap, credit_gap], color=['green', 'red'])
ax2.set_ylabel("Difference ($)")
st.pyplot(fig2)

    # Pie Chart: High Credit Proportion
st.subheader("💳 High Credit Proportion")
fig3, ax3 = plt.subplots()
high_credit_count = (df['AMT_CREDIT'] > 1_000_000).sum()
low_credit_count = (df['AMT_CREDIT'] <= 1_000_000).sum()
ax3.pie([high_credit_count, low_credit_count], labels=['> 1M', '≤ 1M'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
st.pyplot(fig3)
