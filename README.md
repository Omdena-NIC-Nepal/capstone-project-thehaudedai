# Climate Change Impact Assessment and Prediction System for Nepal

### Author: Sashank Niraula

This Streamlit application is an end-to-end data analysis and prediction tool focused on assessing the impacts of climate change in Nepal. The goal is to empower users—particularly data science learners—to explore, preprocess, model, and predict climate-related variables through an interactive and intuitive interface.

You can view the live app here: [Capstone Project App](https://capstone-thehaudedai.streamlit.app/)
## 🌍 Project Overview

The application offers a multi-page interface covering all major steps of a typical data science workflow:

- Data preprocessing
- Exploratory data analysis (EDA)
- Machine learning model training
- Prediction and performance visualization

The project is designed with Nepal’s climate and geography in mind and aims to serve as a starting point for deeper climate-related data analysis initiatives.

## 🔧 Application Structure

```bash
├── Home.py                    # Main landing page
│
├── pages/
│   ├── 1_Data_Preparation.py
│   ├── 2_Exploratory_Analysis.py
│   ├── 3_Modeling.py
│   ├── 4_Prediction.py
│
├── utils/
│   ├── data_loader.py
│   ├── data_preprocessing.py
│   ├── figures.py
│
├── data/                      # Folder to store datasets
├── nepal_map.png             # Map image used in visualizations
├── requirements.txt          # List of dependencies
├── .gitignore
├── README.md                 # This file
```

## ✅ Key Features

### 🔹 Data Preparation

- Handle missing values
- Convert data types of columns
- Reformat DataFrames
- All operations through an interactive UI

### 🔹 Exploratory Data Analysis (EDA)

- Dynamic visualization tools including:
  - Histogram
  - Boxplot
  - Heatmap
- Select variables for X and Y axes using dropdown menus

### 🔹 Modeling

- Choose between Linear Regression and Decision Tree Classifier
- Select input and output columns for training
- View model performance metrics:
  - RMSE
  - MAE
  - R² Score
- Visual comparison of predicted vs actual values

### 🔹 Prediction

- Use trained models to make new predictions
- Display results in both numerical and graphical format

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone <your_repo_url>
   cd <repo_folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run Home.py
   ```

---

## 🛠️ Future Enhancements

- Allow users to upload their own datasets
- Support for multiple file types (CSV, Excel, etc.)
- Enhanced visualization options and user interface improvements
- Integration of shapefiles for geographic mapping
- Better accessibility and mobile-friendly design

## 🎯 Target Audience

This tool is aimed at early-career data scientists or climate researchers looking to apply their skills to real-world environmental challenges in Nepal.
