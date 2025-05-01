import pandas as pd
import plotly.graph_objects as go
import json

# Загрузка данных
with open("data/places.json", encoding="utf-8") as f:
    places = json.load(f)

with open("data/stations.json", encoding="utf-8") as f:
    stations = json.load(f)

with open("data/colors.json", encoding="utf-8") as f:
    biome_colors = json.load(f)

# Преобразуем в DataFrame
df_places = pd.DataFrame(places)
df_stations = pd.DataFrame(stations)

# Объединяем всё в один фрейм для отрисовки точек
df_all = pd.concat([df_places, df_stations], ignore_index=True)

# Добавим цвет
df_all["Color"] = df_all["Biome"].apply(lambda b: biome_colors.get(b, "#aaaaaa"))

# Создаём график
fig = go.Figure()

# Свечение + подписи
for _, row in df_all.iterrows():
    x, z, name, biome, color = row["X"], row["Z"], row["Name"], row["Biome"], row["Color"]

    fig.add_trace(go.Scatter(x=[x], y=[z], mode="markers", marker=dict(size=60, color=color, opacity=0.1), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[x], y=[z], mode="markers", marker=dict(size=30, color=color, opacity=0.3), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="markers+text",
        marker=dict(size=12, color=color, symbol="circle"),
        text=[name],
        textposition="top center",
        name=name,
        hovertemplate=f"<b>{name}</b><br>{biome}<br>X: {x}, Z: {z}<extra></extra>"
    ))

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
fig.write_html("minecraft_map.html")
