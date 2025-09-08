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



# % Male vs Female
# grouped=df['CODE_GENDER']
# grouped


# Avg Age — Defaulters
# Avg Age — Non-Defaulters


# % With Children = % (CNT_CHILDREN > 0)

# With_Children= CNT_CHILDREN df[CNT_CHILDREN>0]  
# With_Children

# Avg Family Size = mean(CNT_FAM_MEMBERS)

# Avg_Family_Size= df['CNT_FAM_MEMBERS'].mean()
# Avg_Family_Size


# % Married vs Single (from NAME_FAMILY_STATUS)
# % Higher Education (Bachelor+)

# df['NAME_EDUCATION_TYPE']

# % Living With Parents (NAME_HOUSING_TYPE == 'With parents')
# % Currently Working (derive from occupation/employment)

# Avg Employment Years
# data1=df['DAYS_EMPLOYED'] 

# EMPLOYMENT_YEARS= -data1/365.25
# EMPLOYMENT_YEARS

# x=EMPLOYMENT_YEARS
# y=len(list(df.columns))

# AVG_EMPLOYMENT_YEARS= x/y
# AVG_EMPLOYMENT_YEARS

# 📊 Calculated Metrics
# 1. % Male vs Female

gender_counts = df['CODE_GENDER'].value_counts(normalize=True) * 100

# 2. Avg Age — Defaulters / Non-Defaulters

df['AGE_YEARS'] = -df['DAYS_BIRTH'] / 365
avg_age_defaulters = df[df['TARGET'] == 1]['AGE_YEARS'].mean()
avg_age_non_defaulters = df[df['TARGET'] == 0]['AGE_YEARS'].mean()

# 3. % With Children
pct_with_children = (df['CNT_CHILDREN'] > 0).mean() * 100

# 4. Avg Family Size
avg_family_size = df['CNT_FAM_MEMBERS'].mean()

# 5. % Married vs Single
married_status = df['NAME_FAMILY_STATUS'].value_counts(normalize=True)[["Single", "not married", "Married", "Civil marriage","Separated","Widow"]] * 100

# 6. % Higher Education (Bachelor’s or higher)
higher_ed = ["Secondary", "secondary special", "Higher education"]
pct_higher_ed = df['NAME_EDUCATION_TYPE'].isin(higher_ed).mean() * 100

# 7. % Living With Parents
pct_living_with_parents = (df['NAME_HOUSING_TYPE'] == 'With parents').mean() * 100

# 8. % Currently Working

# OCCUPATION_TYPE: if it's NaN, assume not working

pct_currently_working = df['OCCUPATION_TYPE'].notna().mean() * 100

# 9. Avg Employment Years
df['YEARS_EMPLOYED'] = -df['DAYS_EMPLOYED'] / 365
avg_employment_years = df['YEARS_EMPLOYED'][df['DAYS_EMPLOYED'] < 0].mean()  # ignore outliers like 365243



# Age & Gender Processing
df['AGE_YEARS'] = -df['DAYS_BIRTH'] / 365
df['YEARS_EMPLOYED'] = -df['DAYS_EMPLOYED'] / 365
df = df[df['DAYS_EMPLOYED'] < 0]  # remove extreme values (e.g. 365243)

st.subheader("👤 Demographic & Lifestyle Metrics")

# Gender Distribution
gender_dist = df['CODE_GENDER'].value_counts(normalize=True) * 100
fig4, ax4 = plt.subplots()
ax4.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', colors=['#66b3ff','#ffcc99'])
ax4.set_title("% Gender Distribution")
st.pyplot(fig4)

# Avg Age
avg_age_def = df[df['TARGET'] == 1]['AGE_YEARS'].mean()
avg_age_nondef = df[df['TARGET'] == 0]['AGE_YEARS'].mean()

# Other metrics
pct_with_children = (df['CNT_CHILDREN'] > 0).mean() * 100
avg_family_size = df['CNT_FAM_MEMBERS'].mean()

# Marital status
married_vs_single = df['NAME_FAMILY_STATUS'].value_counts(normalize=True).get(["Single", "not married", "Married", "Civil marriage","Separated","Widow"], pd.Series()) * 100

# Education
higher_ed_levels = ["Secondary", "secondary special", "Higher education"]
pct_higher_ed = df['NAME_EDUCATION_TYPE'].isin(higher_ed_levels).mean() * 100

# Living with parents
pct_living_parents = (df['NAME_HOUSING_TYPE'] == 'With parents').mean() * 100

# Currently working
pct_working = df['OCCUPATION_TYPE'].notna().mean() * 100
avg_employment_years = df['YEARS_EMPLOYED'].mean()

# Display
st.markdown(f"""
- **Avg Age (Defaulters)**: {avg_age_def:.1f} years  
- **Avg Age (Non-Defaulters)**: {avg_age_nondef:.1f} years  
- **% With Children**: {pct_with_children:.1f}%  
- **Avg Family Size**: {avg_family_size:.2f}  
- **% Higher Education**: {pct_higher_ed:.1f}%  
- **% Living With Parents**: {pct_living_parents:.1f}%  
- **% Currently Working**: {pct_working:.1f}%  
- **Avg Employment Years**: {avg_employment_years:.1f} years  
""")

# Optional: Marital Pie Chart
fig5, ax5 = plt.subplots()
labels = married_vs_single.index if not married_vs_single.empty else ['N/A']
sizes = married_vs_single.values if not married_vs_single.empty else [100]
ax5.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#99ff99', '#ff9999'])
ax5.set_title("% Married vs Single")
st.pyplot(fig5)