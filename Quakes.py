import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go


fig = go.Figure()


# -----------------------------
# 4. Earthquakes layer
# -----------------------------

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
data = requests.get(url).json()

eq_rows = []

for q in data["features"]:
    lon, lat, depth = q["geometry"]["coordinates"]
    mag = q["properties"]["mag"] or 0

    eq_rows.append({
        "lat": lat,
        "lon": lon,
        "mag": mag,
        "place": q["properties"]["place"]
    })


eq = pd.DataFrame(eq_rows)
eq["size"] = np.maximum(eq["mag"], 0) * 4 + 2

fig.add_trace(go.Scattergeo(
    lat=eq["lat"],
    lon=eq["lon"],
    mode="markers",
    marker=dict(
        size=eq["size"],
        color=eq["mag"],
        colorscale="Inferno",
        opacity=0.8,
        colorbar=dict(title="Magnitude")
    ),
    text=eq["place"],
    name="Earthquakes"
))




# -----------------------------
# 5. Plate boundary layer
# -----------------------------

plates_url = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"
plates = requests.get(plates_url).json()

for feature in plates["features"]:
    coords = feature["geometry"]["coordinates"]

    # Some features are MultiLineString
    if feature["geometry"]["type"] == "MultiLineString":
        for line in coords:
            lons, lats = zip(*line)

            fig.add_trace(go.Scattergeo(
                lon=lons,
                lat=lats,
                mode="lines",
                line=dict(width=1, color="cyan"),
                opacity=0.6,
                name="Plate Boundary",
                showlegend=False
            ))

    elif feature["geometry"]["type"] == "LineString":
        lons, lats = zip(*coords)

        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            mode="lines",
            line=dict(width=1, color="cyan"),
            opacity=0.6,
            showlegend=False
        ))


labels = [
    ("Pacific Plate", 0, -150),
    ("North America Plate", 40, -70),
    ("Eurasian Plate", 50, 60),
    ("African Plate", 0, 20),
    ("South America Plate", -20, -60),
]

for name, lat, lon in labels:
    fig.add_trace(go.Scattergeo(
        lat=[lat],
        lon=[lon],
        mode="text",
        text=[name],
        textfont=dict(color="white", size=12),
        showlegend=False
    ))


fig.update_geos(
    projection_type="orthographic",
    showcoastlines=True,
    showcountries=True,
    showland=True,
    showocean=True,
    landcolor="rgb(30,30,30)",
    oceancolor="rgb(10,20,60)",
    lakecolor="rgb(10,20,60)",
    bgcolor="black",
)

fig.update_layout(
    paper_bgcolor="black",
    height=800,
    title="Earthquakes + Tectonic Plate Boundaries"
)



fig.show()