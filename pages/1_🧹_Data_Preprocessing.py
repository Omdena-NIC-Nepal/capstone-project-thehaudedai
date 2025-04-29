import streamlit as st

from utils.data_loader import load_geospatial_data, load_tabular_data
from utils.figures import display_shape_file
from utils.data_preprocessing import get_column_info, melt_dataframe, get_shape

st.set_page_config(
    page_title="Climate Change Dashboard - Data Preprocessing",
    page_icon="🌦️",
    layout="wide",
)

geo_data, shapefile_paths = load_geospatial_data()
tabular_data = load_tabular_data()

data_options = {**geo_data, **tabular_data}

st.title("Data Preprocessing")

# --- Initialize session state ---
if "report_df" not in st.session_state:
    st.session_state.report_df = None
if "monthly_df" not in st.session_state:
    st.session_state.monthly_df = None

if "dtypes_df" not in st.session_state:
    st.session_state.dtypes_df = None
if "missing_df" not in st.session_state:
    st.session_state.missing_df = None

if "report_df_processed" not in st.session_state:
    st.session_state.report_df_processed = None
if "monthly_df_processed" not in st.session_state:
    st.session_state.monthly_df_processed = None

selected_data = st.selectbox(
    "Select a dataset to preview", list(data_options.keys()), index=None
)

# --- Setup session state dataframes based on selection ---
if selected_data:
    if selected_data == "Climate Development Report":
        if st.session_state.report_df is None:
            st.session_state.report_df = data_options[selected_data].copy()
    elif selected_data == "District Wise Monthly Climate":
        if st.session_state.monthly_df is None:
            st.session_state.monthly_df = data_options[selected_data].copy()

# --- Display selected data ---
if selected_data in geo_data:
    map = display_shape_file(data_options[selected_data], selected_data)
    st.pyplot(map)
elif selected_data in tabular_data:
    st.dataframe(data_options[selected_data])
else:
    st.info("👆 Select a dataset from the dropdown to preview it!")


# --- Preprocessing UI ---
if selected_data in tabular_data:
    if selected_data == "Climate Development Report":
        working_df = st.session_state.report_df
    else:
        working_df = st.session_state.monthly_df

    st.subheader("Dataset Overview")

    with st.expander("Column Info: Original Data"):
        st.write(f"Shape: {get_shape(data_options[selected_data])}")

        col1, col2 = st.columns(2)
        dtypes_df, missing_df = get_column_info(data_options[selected_data])

        if st.session_state.dtypes_df is None:
            st.session_state.dtypes_df = dtypes_df.copy()
        if st.session_state.missing_df is None:
            st.session_state.missing_df = missing_df.copy()

        with col1:
            st.markdown("**Data Types**")
            st.dataframe(dtypes_df, use_container_width=True)
        with col2:
            st.markdown("**Missing Values**")
            st.dataframe(missing_df, use_container_width=True)

    st.subheader("Data Reformating")
    reformat_choice = st.radio(
        "Would you like to reformat your dataset to long format?",
        options=["No", "Yes – show formatting options"],
        help=(
            "Reformatting (a.k.a. 'melting') is useful for turning wide datasets "
            "into tidy long-form data. Learn more: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.melt.html"
        ),
    )

    if reformat_choice == "Yes – show formatting options":
        st.warning(
            "If done incorrectly, it may cause errors in data analysis as well as model training",
            icon="⚠️",
        )

        with st.expander("📐 Reformat Data: Convert Wide → Long Format", expanded=True):
            id_vars = st.multiselect(
                "Select columns to keep fixed (ID columns):",
                options=working_df.columns.tolist(),
                help="These columns will remain as they are in the transformed data.",
            )
            col1, col2 = st.columns(2)
            with col1:
                var_name = st.text_input(
                    "Name for the 'Variable' column",
                    placeholder="Year",
                    help="This will be the name of the new column created from the former column headers.",
                )
            with col2:
                value_name = st.text_input(
                    "Name for new column holding values",
                    placeholder="Value",
                    help="This will be the name of the new column containing the actual data values.",
                )
            format_button = st.button("🔄 Format Data", use_container_width=True)

            if format_button:
                if len(id_vars) == len(working_df.columns):
                    st.error("No columns to unpivot. Try selecting fewer ID variables.")
                elif not var_name or not value_name:
                    st.error("Please provide both 'Variable' and 'Value' column names.")
                else:
                    try:
                        working_df = melt_dataframe(
                            working_df, id_vars, var_name, value_name
                        )
                        if selected_data == "Climate Development Report":
                            st.session_state.report_df = working_df
                        elif selected_data == "District Wise Monthly Climate":
                            st.session_state.monthly_df = working_df

                        st.session_state.dtypes_df, st.session_state.missing_df = (
                            get_column_info(working_df)
                        )
                        st.success("Dataset reformatted successfully!")
                        st.subheader("Long Format Data")
                    except Exception as e:
                        st.error(f"Something went wrong while reformatting: {e}")

    st.divider()
    if missing_df["Missing"].sum() > 0:
        st.subheader("Missing Values")
        with st.expander("🧹 Handle Missing Values"):
            st.markdown("Choose how to handle missing values in your dataset:")

            strategy = st.selectbox(
                "Select a strategy",
                [
                    "None",
                    "Drop rows",
                    "Drop columns",
                    "Fill with mean",
                    "Fill with median",
                    "Fill with mode",
                ],
            )

            if strategy != "None":
                apply_missing = st.button("🚀 Apply Missing Value Strategy")
                if apply_missing:
                    try:
                        if strategy == "Drop rows":
                            working_df = working_df.dropna()
                        elif strategy == "Drop columns":
                            working_df = working_df.dropna(axis=1)
                        elif strategy == "Fill with mean":
                            working_df = working_df.fillna(
                                working_df.mean(numeric_only=True)
                            )
                        elif strategy == "Fill with median":
                            working_df = working_df.fillna(
                                working_df.median(numeric_only=True)
                            )
                        elif strategy == "Fill with mode":
                            working_df = working_df.fillna(working_df.mode().iloc[0])

                        if selected_data == "Climate Development Report":
                            st.session_state.report_df = working_df
                        elif selected_data == "District Wise Monthly Climate":
                            st.session_state.monthly_df = working_df

                        st.session_state.dtypes_df, st.session_state.missing_df = (
                            get_column_info(working_df)
                        )

                        st.success(f"Missing value strategy '{strategy}' applied.")
                    except Exception as e:
                        st.error(f"Error applying strategy: {e}")

    st.divider()
    st.subheader("Convert Columns' DataType")
    with st.expander("Convert Column"):
        type_options = [
            "string",
            "int64",
            "float",
            "boolean",
            "category",
            "datetime64[ns]",
            "timedelta[ns]",
            "object",
        ]

        st.write("Choose new data types for each column:")

        col1, col2 = st.columns([1, 3])
        new_type = {}
        dtypes_df = st.session_state.dtypes_df

        for i, r in dtypes_df.iterrows():
            with col1:
                st.text_input(
                    label=f"{r['Column']}",
                    value=f"{r['Column']}",
                    disabled=True,
                    label_visibility="collapsed",
                )

            with col2:
                selected_type = st.selectbox(
                    label=f"{r['Type']}",
                    options=type_options,
                    index=(
                        type_options.index(r["Type"])
                        if r["Type"] in type_options
                        else 2
                    ),
                    label_visibility="collapsed",
                    key=f"select_{r['Column']}",
                )

            new_type[r["Column"]] = selected_type

        apply_datatype = st.button(
            "Apply Data Types To The Columns", use_container_width=True
        )

        if apply_datatype:
            try:
                working_df = working_df.astype(new_type)
                if selected_data == "Climate Development Report":
                    st.session_state.report_df = working_df
                elif selected_data == "District Wise Monthly Climate":
                    st.session_state.monthly_df = working_df

                st.session_state.dtypes_df, st.session_state.missing_df = (
                    get_column_info(working_df)
                )
                st.success("Data types successfully updated.")
            except Exception as e:
                st.error(f"Something went wrong while assigning data types: {e}")

    st.divider()
    st.divider()
    st.subheader("Processed Data Overview")
    with st.expander("Column Info: Processed Data", expanded=True):
        st.write(f"Shape: {get_shape(working_df)}")

        col1, col2 = st.columns(2)
        dtypes_df, missing_df = st.session_state.dtypes_df, st.session_state.missing_df

        with col1:
            st.markdown("**Data Types**")
            st.dataframe(dtypes_df, use_container_width=True)
        with col2:
            st.markdown("**Missing Values**")
            st.dataframe(missing_df, use_container_width=True)

        st.dataframe(working_df, use_container_width=True)

    completion_button = st.button(
        "Complete Preprocessing for this Dataset", use_container_width=True
    )

    if completion_button:
        if selected_data == "Climate Development Report":
            st.session_state.report_df_processed = st.session_state.report_df
        elif selected_data == "District Wise Monthly Climate":
            st.session_state.monthly_df_processed = st.session_state.monthly_df

        st.success("✅ Dataset preprocessing complete and saved.")
