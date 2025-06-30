import pandas as pd
import plotly.graph_objects as go
import json
from typing import List, Dict

icon_by_type = {
    "station": "🚉",
    "village": "🏘️",
    "portal": "🌀",
    "missing": "❓",
    "base": "🛏️",
    "point": "⬛",
    "shipwreck": "⚓",
    "trialchambers": "🗝️",
    "oceanmonument": "🧿"
}


def load_json(filepath: str) -> List[Dict]:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def validate_data(data: List[Dict], source_name: str) -> None:
    required_fields = ["Name", "X", "Z", "Biome", "Type"]
    for row in data:
        for field in required_fields:
            if field not in row:
                raise ValueError(f"⛔ Missing field '{field}' in {source_name}: {row}")


def add_point_trace(fig: go.Figure, row: Dict, icon_by_type: Dict[str, str]) -> None:
    x, z = row["X"], row["Z"]
    name = row["Name"]
    biome = row["Biome"]
    color = row["Color"]
    emoji = icon_by_type.get(row["Type"].lower(), icon_by_type["missing"])

    # Label above
    fig.add_trace(go.Scatter(
        x=[x], y=[z + 10],
        mode="text",
        text=[name],
        textposition="top center",
        textfont=dict(size=14, color='black'),
        showlegend=False,
        hoverinfo="skip"
    ))

    # Main marker
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="markers",
        marker=dict(size=10, color=color, opacity=1),
        name=f"{emoji} {name}",
        hovertemplate=f"<b>{name}</b><br>{biome}<br>X: {x}, Z: {z}<extra></extra>"
    ))

    # Glow
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="markers",
        marker=dict(size=30, color=color, opacity=0.3),
        showlegend=False,
        hoverinfo="skip"
    ))

    # Emoji in center
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="text",
        text=[emoji],
        textposition="middle center",
        textfont=dict(size=15),
        showlegend=False,
        hoverinfo="skip"
    ))


def main() -> None:
    # Load data
    places = load_json("data/places.json")
    stations = load_json("data/stations.json")
    biome_colors = load_json("data/colors.json")

    # Validate data
    validate_data(places, "places.json")
    validate_data(stations, "stations.json")

    # Combine data
    df_places = pd.DataFrame(places)
    df_stations = pd.DataFrame(stations)
    df_all = pd.concat([df_stations, df_places], ignore_index=True)
    df_all["Color"] = df_all["Biome"].apply(lambda b: biome_colors.get(b, "#aaaaaa"))

    # Create figure
    fig = go.Figure()

    # Train route
    fig.add_trace(go.Scatter(
        x=df_stations["X"],
        y=df_stations["Z"],
        mode="lines+markers",
        line=dict(color="gray", width=3, dash="dashdot"),
        marker=dict(size=6, color="black"),
        name="Train route",
        hoverinfo="skip"
    ))

    # Add points
    for _, row in df_all.iterrows():
        add_point_trace(fig, row, icon_by_type)

    # Layout
    fig.update_layout(
        title="Minecraft map",
        xaxis_title="X",
        yaxis_title="Z",
        width=1500,
        height=700,
        dragmode="zoom",
        hovermode="closest"
    )

    # Save as HTML
    fig.write_html("index.html")
    print("✅ Map saved to 'index.html'")


if __name__ == "__main__":
    main()
