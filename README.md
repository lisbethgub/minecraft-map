# Карта сервера Minecraft 🗺️

Интерактивная визуализация важных мест на нашем сервере Minecraft.  
Используется Plotly и Python.

minecraft-map/
├── data/
│   ├── places.json        # все обычные локации (базы, порталы, и т.п.)
│   ├── stations.json      # только станции (для маршрутов)
│   └── colors.json        # цвета биомов
├── map_plot.py            # основной скрипт, который строит карту
├── requirements.txt       # список зависимостей (pandas, plotly и т.д.)
├── README.md              # описание проекта и инструкция
└── minecraft_map.html     # итоговая карта (автоматически создаётся)



## Как запустить

1. Установи зависимости:

pip install -r requirements.txt

2. Запусти скрипт:

python map_plot.py


3. Откроется интерактивная карта в браузере ✨

## Файлы
- `data/places.json` — точки: дома, шахты, порталы
- `data/stations.json` — точки для железной дороги
- `data/colors.json` — цвета для биомов

## Хочешь добавить точку?
1. Добавь её в `places.json`
2. Сделай pull request ✅

