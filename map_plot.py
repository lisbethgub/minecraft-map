import pandas as pd
import plotly.graph_objects as go
import json
from typing import List, Dict

icon_by_type = {
    "station": "🚉",
    "village": "🏘️",
    "portal": "🌀",
    "missing": "❓",
    "base": "🏯",
    "point": "",
    "shipwreck": "⚓",
    "trialchambers": "🗝️",
    "oceanmonument": "🐡",
    "igloo": "❄️",
    "spawn": "🌱",
    "woodlandmansion": "🏚️",
    "bastion": "🌆",
    "lava": "🔥",
    "pumpkins": "🎃"
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
    radius = 80  # радиус биомного круга

    # Цветной круг (биом)
    fig.add_shape(
        type="circle",
        xref="x", yref="y",
        x0=x - radius, y0=z - radius,
        x1=x + radius, y1=z + radius,
        line=dict(width=0),
        fillcolor=color,
        opacity=0.4,
        layer="below"
    )

    # Эмодзи в центре
    fig.add_trace(go.Scatter(
        x=[x],
        y=[z],
        mode="text",
        text=[emoji],
        textfont=dict(size=14),
        name=f"{emoji} {name}",
        hovertemplate=f"<b>{name}</b><br>{biome}<br>X: {x}, Z: {z}<extra></extra>"
    ))

    # Название 
    fig.add_trace(go.Scatter(
        x=[x],
        y=[z - 40],
        mode="text",
        text=[name],
        textfont=dict(size=10, color="black"),
        showlegend=False,
        hoverinfo="skip"
    ))


def main() -> None:
    # Загрузка данных
    places = load_json("data/places.json")
    stations = load_json("data/stations.json")
    biome_colors = load_json("data/colors.json")

    # Проверка данных
    validate_data(places, "places.json")
    validate_data(stations, "stations.json")

    # Объединение
    df_places = pd.DataFrame(places)
    df_stations = pd.DataFrame(stations)
    df_all = pd.concat([df_stations, df_places], ignore_index=True)
    df_all["Color"] = df_all["Biome"].apply(lambda b: biome_colors.get(b, "#aaaaaa"))

    # Создание карты
    fig = go.Figure()

    # Маршрут поезда
    fig.add_trace(go.Scatter(
        x=df_stations["X"],
        y=df_stations["Z"],
        mode="lines+markers",
        line=dict(color="gray", width=3, dash="dashdot"),
        marker=dict(size=6, color="black"),
        name="Train route",
        hoverinfo="skip"
    ))

    # Добавление точек
    for _, row in df_all.iterrows():
        add_point_trace(fig, row, icon_by_type)

    # Настройки графика
    fig.update_layout(
        title="Minecraft map",
        xaxis_title="X",
        yaxis_title="Z",
        width=1000,
        height=1000,
        dragmode="zoom",
        hovermode="closest"
    )

    # 👇 фиксированное соотношение осей — настоящие круги
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    # Сохранение
    fig.write_html("index.html")
    print("✅ Map saved to 'index.html'")


if __name__ == "__main__":
    main()
