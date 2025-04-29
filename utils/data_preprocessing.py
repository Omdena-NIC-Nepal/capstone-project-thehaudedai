import pandas as pd


def get_shape(df: pd.DataFrame):
    """Returns shape as a formatted string."""
    return f"{df.shape[0]} rows × {df.shape[1]} columns"


def get_column_info(df: pd.DataFrame):
    """Returns column data types and missing values."""
    dtypes = df.dtypes.rename("Type").reset_index().rename(columns={"index": "Column"})
    missing = (
        df.isna()
        .sum()
        .rename("Missing")
        .reset_index()
        .rename(columns={"index": "Column"})
    )
    return dtypes, missing


def get_meltable_columns(df: pd.DataFrame, id_vars: list):
    """Returns columns that can be melted (i.e. not in id_vars)."""
    return [col for col in df.columns if col not in id_vars]


def melt_dataframe(df: pd.DataFrame, id_vars: list, var_name: str, value_name: str):
    """Melts the dataframe into long format."""
    return pd.melt(
        df,
        id_vars=id_vars,
        value_vars=get_meltable_columns(df, id_vars),
        var_name=var_name,
        value_name=value_name,
    )
