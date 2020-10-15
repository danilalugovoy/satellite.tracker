# Satellite tracker in Python
![](https://img.shields.io/badge/Python-3.8.3-orange)

## Description
Код для получения информации о спутнике, использующий n2yo.com.
Сейчас в базе данных мало спутников, вы можете добавить их самостоятельно.

## Examples
```python
# Импорт класса Tracker
from satellite import Tracker

# Создание объекта track
track = Tracker('Москва', 'NOAA 1')

# Получение информации
print(track.getSatCoord()) # Координаты (массив с lat (0) lon (1))
print(track.getSatAltitude()) # Высота спутника
print(track.getSatAzimuth()) # Азимут спутника
print(track.getSatInterCode()) # Международный код спутника
print(track.getSatPerigee()) # Перигей
print(track.getSatApogee()) # Апогей
print(track.getSatIncl()) # Наклон в градусах
print(track.getSatPeriod()) # Период оборота вокруг Земли в минутах
print(track.getSatSource()) # Страна, запустившая спутник
print(track.getSatLaunchSite()) # Космодром, с которого был запущен спутник
print(track.getSatVisual()) # Когда спутник можно будет увидеть над городом, который вы указали при создании объекта. Массив со временем (начало прохода (0) и конец прохода (1)). Если выдало None - информации нет.
print(track.getSatRadio()) # Когда спутник будет испускать радио-сигнал городом, который вы указали при создании объекта. Массив со временем (начало прохода (0) и конец прохода (1). Если выдало None - информации нет.
```
