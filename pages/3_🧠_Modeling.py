import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
import pandas as pd
import numpy as np
import time
import pickle

st.title("🧠 Model Training and Evaluation")

# Step 1: Choose available dataset
available_datasets = {
    "Climate Development Report": st.session_state.get("report_df_processed"),
    "District Wise Monthly Climate": st.session_state.get("monthly_df_processed"),
}

available_datasets = {k: v for k, v in available_datasets.items() if v is not None}

if not available_datasets:
    st.warning("⚠️ No processed datasets found. Please complete preprocessing first.")
    st.stop()

selected_dataset = st.selectbox(
    "Choose a processed dataset", list(available_datasets.keys()), index=1
)
df = available_datasets[selected_dataset]
st.dataframe(df.head())

# Step 2: Feature Selection
st.subheader("🔢 Feature Selection")

all_columns = df.columns.tolist()

with st.form("feature_selection_form"):
    st.write("Select input feature columns (X):")

    selected_x_columns = []
    num_cols = 4
    num_rows = (len(all_columns) + num_cols - 1) // num_cols

    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            idx = row * num_cols + col_idx
            if idx < len(all_columns):
                col_name = all_columns[idx]
                if cols[col_idx].checkbox(col_name, key=f"x_{col_name}"):
                    selected_x_columns.append(col_name)

    y_column_options = [col for col in all_columns if col not in selected_x_columns]
    y_column = st.selectbox(
        "Select target column (Y)", options=y_column_options, index=None
    )

    submitted = st.form_submit_button("Confirm Feature Selection")

if submitted:
    st.session_state["x_columns"] = selected_x_columns
    st.session_state["y_column"] = y_column
    st.success(f"Selected X: {selected_x_columns}, Y: {y_column}")

# Retrieve from session state
x_columns = st.session_state.get("x_columns")
y_column = st.session_state.get("y_column")

if not x_columns or not y_column:
    st.warning("Please select features and confirm to proceed.")
    st.stop()

# Step 3: Train-Test Split
st.subheader("🧪 Train-Test Split")
test_size_percent = st.slider(
    "Test size (%)", min_value=10, max_value=50, value=20, step=5
)
test_size = test_size_percent / 100

# Step 4: Model Selection
st.subheader("🧮 Model Selection")
model_choice = st.selectbox("Choose a model", ["Linear Regression", "Decision Tree"])

# Step 5: Train model
train_button = st.button("🚀 Train Model")

if train_button:
    with st.spinner("Training the model..."):
        time.sleep(1)  # Simulate loading
        X = df[x_columns]
        y = df[y_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        if model_choice == "Linear Regression":
            model = LinearRegression()
        else:
            model = DecisionTreeRegressor(random_state=42)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Step 6: Evaluation
        st.success("✅ Model training completed!")
        st.subheader("📊 Evaluation Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("R² Score", round(r2_score(y_test, y_pred), 4))
        with col2:
            rmse = root_mean_squared_error(y_test, y_pred)
            st.metric("RMSE", round(rmse, 4))
        with col3:
            st.metric("MAE", round(mean_absolute_error(y_test, y_pred), 4))

        result_df = pd.DataFrame({"Actual": y_test.values, "Predicted": y_pred})
        st.dataframe(result_df.head())

        st.line_chart(result_df.head(200))

        # Save and allow download
        model_filename = "trained_model.pkl"
        with open(model_filename, "wb") as f:
            pickle.dump(model, f)

        with open(model_filename, "rb") as f:
            st.download_button(
                label="📥 Download Trained Model",
                data=f,
                file_name=model_filename,
                mime="application/octet-stream",
                use_container_width=True,
            )
