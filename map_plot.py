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
    "trialchambers": "🗝️"
}

# Загрузка данных
with open("data/places.json", encoding="utf-8") as f:
    places = json.load(f)

with open("data/stations.json", encoding="utf-8") as f:
    stations = json.load(f)

with open("data/colors.json", encoding="utf-8") as f:
    biome_colors = json.load(f)

# Чекаем корректны ли данные
def validate_data(data: List[Dict], source_name: str) -> None:
    required_fields = ["Name", "X", "Z", "Biome", "Type"]
    for row in data:
        for field in required_fields:
            if field not in row:
                raise ValueError(f"⛔ Отсутствует поле '{field}' в {source_name}: {row}")

validate_data(places, "places.json")
validate_data(stations, "stations.json")

# Преобразуем в DataFrame
df_places = pd.DataFrame(places)
df_stations = pd.DataFrame(stations)

# Объединяем всё в один фрейм для отрисовки точек
df_all = pd.concat([df_stations, df_places], ignore_index=True)

# Добавим цвет
df_all["Color"] = df_all["Biome"].apply(lambda b: biome_colors.get(b, "#aaaaaa"))

# Создаём график
fig = go.Figure()


# Линия между станциями
fig.add_trace(go.Scatter(
    x=df_stations["X"],
    y=df_stations["Z"],
    mode="lines+markers",
    line=dict(color="gray", width=3, dash="dashdot"),
    marker=dict(size=6, color="black"),
    name="Train route",
    hoverinfo="skip"
))

for _, row in df_all.iterrows():
    x, z = row["X"], row["Z"]
    name = row["Name"]
    biome = row["Biome"]
    color = row["Color"]
    emoji = icon_by_type.get(row["Type"].lower(), icon_by_type["missing"])

    # Название сверху
    fig.add_trace(go.Scatter(
        x=[x], y=[z + 10],
        mode = "text",
        text=[name],
        textposition="top center",
        textfont=dict(size=14, color='black'),
        showlegend=False,
        hoverinfo="skip"
    ))

    #  Свечение (двойной маркер)
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="markers",
        marker=dict(size=10, color=color, opacity=1),
        name=f"{emoji} {name}",
        hovertemplate=f"<b>{name}</b><br>{biome}<br>X: {x}, Z: {z}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=[x], y=[z], 
        mode="markers", 
        marker=dict(size=30, color=color, opacity=0.3),
        showlegend=False,
        hoverinfo="skip"
    ))


for _, row in df_all.iterrows():
    x, z = row["X"], row["Z"]
    name = row["Name"]
    biome = row["Biome"]
    color = row["Color"]
    emoji = icon_by_type.get(row["Type"].lower(), icon_by_type["missing"])

     # Эмодзи по центру
    fig.add_trace(go.Scatter( x=[x], y=[z],
        mode="text",
        text=[emoji],
        textposition="middle center",
        textfont=dict(size=15),
        showlegend=False,
        hoverinfo="skip"
    ))

# Настройки графика
fig.update_layout(
    title="Minecraft map",
    xaxis_title="X",
    yaxis_title="Z",
    width=900,
    height=700,
    dragmode="zoom",
    hovermode="closest"
)

# Сохраняем в HTML
fig.write_html("index.html")


