import streamlit as st
import pickle
import numpy as np

st.title("🔮 Model Prediction")

# Step 1: Load the trained model from session state
model_filename = "trained_model.pkl"

try:
    with open(model_filename, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.warning("⚠️ No trained model found. Please train a model first.")
    st.stop()

# Step 2: Retrieve x_columns and y_column from session state
x_columns = st.session_state.get("x_columns")
if not x_columns:
    st.warning("⚠️ No feature columns found. Please train a model first.")
    st.stop()

# Step 3: Create a form for input features
st.subheader("🔢 Enter Input Features")
input_data = {}

with st.form("input_form"):
    for col_name in x_columns:
        # Check if the column is numeric or categorical and create appropriate input widget
        column_data_type = st.session_state.get(
            col_name, "numeric"
        )  # Default to numeric if not found
        if column_data_type == "numeric":
            input_data[col_name] = st.number_input(
                f"Enter value for {col_name}", value=0.0
            )
        else:
            input_data[col_name] = st.selectbox(
                f"Select value for {col_name}",
                options=["Option 1", "Option 2", "Option 3"],
            )

    # Submit button to trigger prediction
    submitted = st.form_submit_button("🔮 Predict")

# Step 4: Make prediction and display the result
if submitted:
    # Prepare the input features for prediction
    input_features = np.array([list(input_data.values())]).reshape(1, -1)

    with st.spinner("Making prediction..."):
        prediction = model.predict(input_features)

    # Step 5: Display prediction result
    st.success("✅ Prediction complete!")
    st.subheader("📊 Prediction Results")
    st.write(f"The predicted value for the target column is: {prediction[0]}")
