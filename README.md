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
print(track.getSatCoord())
print(track.getSatAltitude())
print(track.getSatAzimuth())
print(track.getSatInterCode())
print(track.getSatPerigee())
print(track.getSatApogee())
print(track.getSatIncl())
print(track.getSatPeriod())
print(track.getSatSource())
print(track.getSatLaunchSite())
print(track.getSatVisual())
print(track.getSatRadio())
```
