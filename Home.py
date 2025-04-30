import streamlit as st

# Page config (adds tab title, icon, layout)
st.set_page_config(
    page_title="Climate Change Dashboard - Nepal", page_icon="🌦️", layout="wide"
)

# Main title
st.title("🌦️ Climate Change Impact Dashboard – Nepal ")

# Subheader
st.write(
    "#### A data-driven platform to assess, analyze, and predict climate change impacts in Nepal."
)
st.image("nepal_map.png", width=900)
# Divider
st.write("---")

# Project Overview Section
with st.container():
    st.write("### 📌 Project Overview")
    st.write(
        """
    This dashboard is built to help researchers, students, and policy-makers explore climate-related issues in Nepal using real-world data.

    The platform supports:
    - Data preprocessing and cleaning
    - Exploratory data analysis (EDA)
    - Geospatial visualization of climate vulnerabilities
    - Machine learning models for climate prediction
    - Natural Language Processing (NLP) on climate news
    - Report generation and user feedback collection. 
    """
    )

st.write("👉 Use the sidebar to navigate through the sections.")

# Footer
st.write("---")
st.write(
    "🚀 Built by Sashank Niraula | 📬 Contact: haudedai@proton.me | 🧑‍🔬 For academic and policy use"
)
