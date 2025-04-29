import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Climate Change Dashboard - Data Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Data Analysis")

# --- Check if processed datasets exist ---
if (
    st.session_state.get("report_df_processed") is None
    and st.session_state.get("monthly_df_processed") is None
):
    st.warning("⚠️ Please complete data preprocessing before analyzing the data.")
    st.stop()

# --- Dataset Selection ---
dataset_options = {}
if st.session_state.get("report_df_processed") is not None:
    dataset_options["Climate Development Report"] = st.session_state.report_df_processed
if st.session_state.get("monthly_df_processed") is not None:
    dataset_options["District Wise Monthly Climate"] = (
        st.session_state.monthly_df_processed
    )

selected_data = st.selectbox("Select a processed dataset", list(dataset_options.keys()))

df = dataset_options[selected_data]

st.write(f"### Dataset: {selected_data}")
st.dataframe(df, use_container_width=True)

# --- Summary Statistics ---
st.subheader("📈 Descriptive Statistics")
st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

# --- Column Selection ---
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
if not numeric_cols:
    st.warning("No numeric columns available for analysis.")
    st.stop()

col1, col2 = st.columns(2)

# --- Histogram ---
with col1:
    st.write("### Histogram")
    hist_col = st.selectbox("Select a column for histogram", numeric_cols)
    fig, ax = plt.subplots()
    sns.histplot(df[hist_col].dropna(), kde=True, ax=ax)
    st.pyplot(fig)

# --- Line Plot ---
with col2:
    st.write("### Line Plot")
    time_col = st.selectbox("Select x-axis (e.g. time or ID)", df.columns)
    value_col = st.selectbox("Select y-axis (numeric)", numeric_cols, key="line_plot")
    fig, ax = plt.subplots()
    df_sorted = df.sort_values(by=time_col)
    ax.plot(df_sorted[time_col], df_sorted[value_col])
    ax.set_xlabel(time_col)
    ax.set_ylabel(value_col)
    ax.set_title(f"{value_col} over {time_col}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Box Plot ---
st.write("### Box Plot")
box_col = st.selectbox("Select column for box plot", numeric_cols, key="box_plot")
fig, ax = plt.subplots()
sns.boxplot(y=df[box_col], ax=ax)
st.pyplot(fig)

# --- Correlation Heatmap ---
st.write("### 🔥 Correlation Heatmap")
if len(numeric_cols) > 1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.info("Not enough numeric columns for correlation heatmap.")
