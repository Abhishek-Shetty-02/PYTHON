from Utils.load_data import load_data
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


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


def display_default_analysis(df):
    st.header("🚨 Default Risk Analysis")

    if "TARGET" not in df.columns:
        st.warning("TARGET column not found in dataset.")
        return

    # --- Defaulters subset ---
    df_default = df[df["TARGET"] == 1]

    # --- Core Metrics ---
    total_defaults = df["TARGET"].sum()
    default_rate = df["TARGET"].mean() * 100

    col1, col2 = st.columns(2)
    col1.metric("Total Defaults", f"{int(total_defaults):,}")
    col2.metric("Default Rate (%)", f"{default_rate:.2f}")

    # --- Helper: Plot Default Rate by Category ---
    def plot_grouped_default_rate(by_col, title):
        if by_col not in df.columns:
            st.info(f"❌ Column '{by_col}' not found.")
            return

        grouped = df.groupby(by_col)["TARGET"].mean().sort_values(ascending=False) * 100

        # Display DataFrame
        st.subheader(f"📊 Default Rate by {title}")
        st.dataframe(grouped.rename("Default Rate (%)").round(2))

        # Matplotlib Bar Chart
        fig, ax = plt.subplots()
        grouped.plot(kind="bar", color="salmon", edgecolor="black", ax=ax)
        ax.set_ylabel("Default Rate (%)")
        ax.set_title(f"Default Rate by {title}")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

    # --- Grouped Visuals ---
    plot_grouped_default_rate("Gender", "Gender")
    plot_grouped_default_rate("Education", "Education")
    plot_grouped_default_rate("Family Status", "Family Status")
    plot_grouped_default_rate("Housing", "Housing Type")

    # --- Averages for Defaulters ---
    st.subheader("📉 Averages — Defaulters Only")
    metrics = {
        "Avg Annual Income": df_default["AMT_INCOME_TOTAL"].mean() if "AMT_INCOME_TOTAL" in df_default else None,
        "Avg Credit Amount": df_default["AMT_CREDIT"].mean() if "AMT_CREDIT" in df_default else None,
        "Avg Annuity Amount": df_default["AMT_ANNUITY"].mean() if "AMT_ANNUITY" in df_default else None,
        "Avg Employment Years": df_default["EMPLOYMENT_YEARS"].mean() if "EMPLOYMENT_YEARS" in df_default else None,
    }

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    cols = [col1, col2, col3, col4]

    for i, (label, value) in enumerate(metrics.items()):
        if value is not None and not pd.isna(value):
            formatted = f"${value:,.0f}" if "Income" in label or "Credit" in label or "Annuity" in label else f"{value:.1f} yrs"
            cols[i].metric(label, formatted)
        else:
            cols[i].metric(label, "N/A")


display_default_analysis(df)