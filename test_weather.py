from wthr import weather as weather
import pandas as pd

weather = weather()
df = pd.DataFrame(weather.getHourlyTemps(station='KEVV')['temps'])

print(df.head())