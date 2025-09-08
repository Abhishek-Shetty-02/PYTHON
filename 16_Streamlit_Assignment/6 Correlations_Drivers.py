from Utils.load_data import load_data
import numpy as np
import pandas as pd
import streamlit as st

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


# Top 5 +Corr with TARGET (list)
# Top 5 −Corr with TARGET (list)
# Most correlated with Income
# Most correlated with Credit
# Corr(Income, Credit)
# Corr(Age, TARGET)
# Corr(Employment Years, TARGET)
# Corr(Family Size, TARGET)
# Variance Explained by Top 5 Features (proxy via |corr|)
# # Features with |corr| > 0.5

import streamlit as st
import pandas as pd
import numpy as np

def display_correlation_insights(df):
    st.header("📈 Correlation Insights")

    # Filter only numeric columns and drop NaNs
    numeric_df = df.select_dtypes(include=[np.number]).dropna()

    # Correlation matrix
    corr_matrix = numeric_df.corr()

    if "TARGET" not in corr_matrix.columns:
        st.warning("TARGET column missing from numeric data. Cannot compute correlations.")
        return

    # --- Top +ve and −ve correlations with TARGET ---
    target_corr = corr_matrix["TARGET"].drop("TARGET")
    top_pos_corr = target_corr.sort_values(ascending=False).head(5)
    top_neg_corr = target_corr.sort_values().head(5)

    st.subheader("🔝 Top Correlated Features with TARGET")
    col1, col2 = st.columns(2)
    col1.write("**Top 5 + Correlations**")
    col1.dataframe(top_pos_corr.round(3))
    col2.write("**Top 5 − Correlations**")
    col2.dataframe(top_neg_corr.round(3))

    # --- Most correlated with Income ---
    income_corr = corr_matrix["AMT_INCOME_TOTAL"].drop("AMT_INCOME_TOTAL") if "AMT_INCOME_TOTAL" in corr_matrix else None
    credit_corr = corr_matrix["AMT_CREDIT"].drop("AMT_CREDIT") if "AMT_CREDIT" in corr_matrix else None

    most_corr_with_income = income_corr.abs().sort_values(ascending=False).idxmax() if income_corr is not None else "N/A"
    most_corr_with_credit = credit_corr.abs().sort_values(ascending=False).idxmax() if credit_corr is not None else "N/A"

    # --- Individual Correlations ---
    def safe_corr(col1, col2):
        if col1 in corr_matrix.columns and col2 in corr_matrix.columns:
            return corr_matrix.loc[col1, col2]
        else:
            return np.nan

    corr_income_credit = safe_corr("AMT_INCOME_TOTAL", "AMT_CREDIT")
    corr_age_target = safe_corr("AGE_YEARS", "TARGET")
    corr_emp_target = safe_corr("EMPLOYMENT_YEARS", "TARGET")
    corr_famsize_target = safe_corr("CNT_FAM_MEMBERS", "TARGET") if "CNT_FAM_MEMBERS" in corr_matrix else np.nan

    # --- Variance Explained Proxy (Top 5 features correlated with TARGET) ---
    variance_proxy = (target_corr.abs().sort_values(ascending=False).head(5) ** 2).sum()

    # --- Count of Features with |corr| > 0.5 ---
    high_corr_count = (target_corr.abs() > 0.5).sum()

    # --- Display Summary ---
    st.subheader("📌 Summary Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Most Corr. w/ Income", most_corr_with_income)
    col2.metric("Most Corr. w/ Credit", most_corr_with_credit)
    col3.metric("Corr(Income, Credit)", f"{corr_income_credit:.3f}" if not pd.isna(corr_income_credit) else "N/A")

    col4, col5, col6 = st.columns(3)
    col4.metric("Corr(Age, Target)", f"{corr_age_target:.3f}" if not pd.isna(corr_age_target) else "N/A")
    col5.metric("Corr(Emp. Years, Target)", f"{corr_emp_target:.3f}" if not pd.isna(corr_emp_target) else "N/A")
    col6.metric("Corr(Family Size, Target)", f"{corr_famsize_target:.3f}" if not pd.isna(corr_famsize_target) else "N/A")

    col7, col8 = st.columns(2)
    col7.metric("Variance Explained (Top 5)", f"{variance_proxy:.3f}")
    col8.metric("# Features |corr| > 0.5", high_corr_count)


display_correlation_insights(df)