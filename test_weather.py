from wthr import weather as weather
import pandas as pd

weather = weather()
df = pd.DataFrame(weather.getHourlyTemps(station='KEVV')['temps'])
df['temp'] = df['temp'].round(0)

print(weather.getStationHourlyForecast(station='KEVV'))