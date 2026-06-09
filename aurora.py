import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- Fetch data ---
url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
data = requests.get(url, timeout=10).json()

coords = data["coordinates"]

# --- Build dataframe ---
df = pd.DataFrame(coords, columns=["lon", "lat", "prob"])

# ---  DOWNSAMPLE (main performance fix) ---
# Adjust step size: higher = faster, lower = more detail
df = df.iloc[::3].reset_index(drop=True)

# Optional: remove ultra-low probability noise (reduces clutter)
df = df[df["prob"] > 5]

# --- Figure ---
fig = go.Figure()

fig.add_trace(
    go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        marker=dict(
            size=2,                 # smaller = faster
            opacity=1,           # reduces GPU/CPU load
            color=df["prob"],
            colorscale="Viridis",
            showscale=False        #  removing colorbar = big speed boost
        ),
        hovertemplate="Lat: %{lat}<br>Lon: %{lon}<br>Prob: %{marker.color:.1f}%<extra></extra>"
    )
)

# --- Globe settings (keep minimal for performance) ---
fig.update_geos(
    projection_type="orthographic",
    showland=False,
    showocean=False,
    showcountries=False,
    showcoastlines=True,
    showlakes=False,
    coastlinecolor="lime",
    coastlinewidth=.4,
    showframe=False,
    bgcolor="black"
)

# --- Layout optimization ---
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="black",
    geo=dict(bgcolor="black")
)




fig.show()