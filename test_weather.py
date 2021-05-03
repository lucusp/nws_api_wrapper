from wthr import weather as weather

weather = weather()

print(weather.getHourlyTemps(station='KEVV'))