import pandas as pd
import plotly.graph_objects as go
import json
import base64
import os

# Загрузка данных
with open("data/places.json", encoding="utf-8") as f:
    places = json.load(f)

with open("data/stations.json", encoding="utf-8") as f:
    stations = json.load(f)

with open("data/colors.json", encoding="utf-8") as f:
    biome_colors = json.load(f)

# Чекаем корректны ли данные
def validate_data(data, source_name):
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
df_all = pd.concat([df_places, df_stations], ignore_index=True)

# Добавим цвет
df_all["Color"] = df_all["Biome"].apply(lambda b: biome_colors.get(b, "#aaaaaa"))

# Создаём график
fig = go.Figure()



def encode_image(image_file):
    with open(image_file, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

# Добавим иконки
for _, row in df_all.iterrows():
    x, z = row["X"], row["Z"]
    label = row["Name"]
    icon_type = row["Type"].lower()
    icon_path = f"icons/{icon_type}.png"

    if os.path.exists(icon_path):
        fig.add_layout_image(
            dict(
                source=encode_image(icon_path),
                x=x,
                y=z,
                xref="x",
                yref="y",
                sizex=40,
                sizey=40,
                xanchor="center",
                yanchor="middle",
                layer="above"
            )
        )
    else:
        # Используем иконку "вопрос" как заглушку
        fallback_icon_path = "icons/missing.png"
        if os.path.exists(fallback_icon_path):
            fig.add_layout_image(
                dict(
                    source=encode_image(fallback_icon_path),
                    x=x,
                    y=z,
                    xref="x",
                    yref="y",
                    sizex=40,
                    sizey=40,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
                )
            )
        else:
            print(f"⚠️ Icon not found: {icon_path}, and fallback icon missing too: {fallback_icon_path}")


# Свечение + подписи
for _, row in df_all.iterrows():
    x, z, name, biome, color = row["X"], row["Z"], row["Name"], row["Biome"], row["Color"]

    fig.add_trace(go.Scatter(x=[x], y=[z], mode="markers", marker=dict(size=60, color=color, opacity=0.1), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[x], y=[z], mode="markers", marker=dict(size=30, color=color, opacity=0.3), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=[x], y=[z],
        mode="markers+text",
        marker=dict(size=17, color=color, symbol="circle"),
        text=[name],
        textposition="top center",
        name=name,
        hovertemplate=f"<b>{name}</b><br>{biome}<br>X: {x}, Z: {z}<extra></extra>"
    )
    )

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
fig.write_html("index.html")


