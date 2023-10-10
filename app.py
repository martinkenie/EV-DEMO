from flask import Flask, render_template, request, jsonify
import geopandas as gpd
from shapely.geometry import Point
import json

app = Flask(__name__)

# Load the charging points data
charging_points_gdf = gpd.read_file("charging_points.shp")
charging_points_gdf.crs = "EPSG:32636"
charging_points_gdf = charging_points_gdf.to_crs(epsg=4326)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_nearest", methods=["POST"])
def get_nearest():
    try:
        user_lat = float(request.form.get("latitude"))
        user_lon = float(request.form.get("longitude"))
        user_point = Point(user_lon, user_lat)
        # Ensure user point is in the same CRS as charging_points_gdf
        user_point = gpd.GeoSeries([user_point], crs="EPSG:4326")

        distances = charging_points_gdf.distance(user_point.iloc[0])
        nearest_idx = distances.idxmin()
        nearest_point = charging_points_gdf.loc[nearest_idx]

        # Send the coordinates to the HTML
        return render_template("index.html", lat=nearest_point.geometry.y, lon=nearest_point.geometry.x)
    except Exception as e:
        return str(e)  # To display the error in the browser for debugging


if __name__ == "__main__":
    app.run(debug=True)
