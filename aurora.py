import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
import numpy as np

# Load custom stylesheet from local file
with open("stylesheet.css", "r") as f:
    CUSTOM_CSS = f.read()

st.set_page_config(
    page_title="Aurora Seeker",
    layout="centered",
    page_icon="🌌",
    initial_sidebar_state="expanded"
)

# Apply the loaded stylesheet
st.markdown(f'<style>{CUSTOM_CSS}</style>', unsafe_allow_html=True)

# --- Header with styled text ---
st.markdown("""
<div class="aurora-header">
  <h1 class="title-gradient">AURORA SEEKER</h1>
  <p class="subtitle-styled">Real-time OVATION aurora data visualization</p>
</div>
""", unsafe_allow_html=True)

# --- Status indicator with styled text ---
st.markdown("""
<div class="status-badge">
  <div class="status-dot"></div>
  <span class="live-indicator">LIVE DATA FEED</span>
</div>
""", unsafe_allow_html=True)

# --- Globe visualization card container ---
st.markdown("""
<div class="terminal-container">
""", unsafe_allow_html=True)

# --- Fetch data ---
@st.cache_data(ttl=30)
def fetch_aurora_data():
    url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    try:
        response = requests.get(url, timeout=15).json()
        return response["coordinates"]
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        return None

coords = fetch_aurora_data()

if coords is None:
    st.error("Unable to fetch aurora data. Please refresh the page.")
    st.stop()

# --- Build dataframe ---
df = pd.DataFrame(coords, columns=["lon", "lat", "prob"])

# Downsample for performance while maintaining visual quality
step_size = 5
df = df.iloc[::step_size].reset_index(drop=True)

# Filter noise - keep only meaningful probability values
df = df[df["prob"] > 3]

# --- Globe Visualization with styled container ---
fig = go.Figure(data=[
    # Color-coded markers showing probability intensity
    go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        marker=dict(
            symbol="circle-open",
            size=8,
            color=df["prob"],
            colorscale="Viridis",
            showscale=False,
            opacity=0.85,
            line=dict(width=1.5, color='rgba(255,255,255,0.3)')
        ),
        hovertemplate="<b>%{text}</b><br>Lon: %{lon:.2f}<br>Lat: %{lat:.2f}<br>Prob: %{marker.color:.1f}%<extra></extra>"
    )
])

fig.update_geos(
    projection_type="orthographic",
    showland=True,
    showocean=True,
    oceancolor="#0a1628",
    showcountries=True,
    countrycolor="#12d500",
    countrywidth=1.5,
    showcoastlines=True,
    coastlinecolor="rgba(255,255,255,0.3)",
    coastlinewidth=0.5,
    bgcolor="rgba(10, 15, 30, 0.8)",
    landcolor="rgba(255, 255, 255, 0.03)",
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    geo=dict(
        showframe=False,
        fitbounds=None
    ),
    hovermode="closest",
    height=700
)

# Add title to the plot
fig.add_annotation(
    x=0, y=0,
    text="Aurora Probability Distribution",
    showarrow=False,
    font=dict(size=14, family="Inter", color="rgba(255,255,255,0.9)")
)

st.plotly_chart(fig, use_container_width=True, config={'responsive': True})


# --- Footer with modern design ---
st.markdown("""
<div class="terminal-footer">
  <p>← Aurora Stream Powered by NOAA/SWPC OVATION Model →</p>
</div>
""", unsafe_allow_html=True)

# --- Closing globe container ---
st.markdown("</div>", unsafe_allow_html=True)