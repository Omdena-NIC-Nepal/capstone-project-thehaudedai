import pandas as pd
import geopandas as gpd


def load_geospatial_data():
    shapefile_paths = {
        "National Boundary": "data/national_boundary_shape_file/national_boundary.shp",
        "Provincial Boundary": "data/provincial_boundary_shape_file/provincial_boundary.shp",
        "District Boundary (SHP)": "data/district_boundary_shape_file/district_boundary.shp",
        "River Line": "data/river_line_shape_file/river_line.shp",
        "River Polygon": "data/river_polygon_shape_file/river_polygon.shp",
        "District Boundary (GeoJSON)": "data/district.geojson",
    }

    geo_data = {name: gpd.read_file(path) for name, path in shapefile_paths.items()}

    # Harmonize CRS if applicable
    if (
        "District Boundary (GeoJSON)" in geo_data
        and "District Boundary (SHP)" in geo_data
    ):
        geo_data["District Boundary (GeoJSON)"] = geo_data[
            "District Boundary (GeoJSON)"
        ].to_crs(geo_data["District Boundary (SHP)"].crs)

    return geo_data, shapefile_paths


def load_tabular_data():
    tabular_paths = {
        "District Wise Monthly Climate": "data/nepal_district_monthly_climate_data.csv",
        "Climate Development Report": "data/Nepal_Climate_Development_Report.xlsx",
    }

    tabular_data = {
        "District Wise Monthly Climate": pd.read_csv(
            tabular_paths["District Wise Monthly Climate"]
        ),
        "Climate Development Report": pd.read_excel(
            tabular_paths["Climate Development Report"]
        ),
    }

    return tabular_data
