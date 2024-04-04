import requests

def get_point_data(latitude, longitude):
  """
  Retrieves point data from the NOAA NWS API based on latitude and longitude.
  Returns:
      dict: Point data dictionary or None if broke.
  """
  url = f"https://api.weather.gov/points/{latitude},{longitude}"
  response = requests.get(url)
  if response.ok:
    return response.json()
  else:
    print(f"Error retrieving point data: {response.text}")
    return None
   ## self check to see whats wrong if not outputting data 
def get_grid_forecast(latitude, longitude):
  """
  Retrieves forecast data from the NOAA NWS API based on latitude and longitude.
  Returns:
      str: Forecast description or None if request fails.
  """
  # Retrieve point data to get office, gridX, gridY, and relative location
  point_data = get_point_data(latitude, longitude)
  if not point_data:
    return None

  office = point_data["properties"]["gridId"]
  gridX = point_data["properties"]["gridX"]
  gridY = point_data["properties"]["gridY"]
  relative_location = point_data["properties"]["relativeLocation"]["properties"]["city"]

  # Construct the URL for the forecast API endpoint
  url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

  # Send a GET request to the forecast API endpoint
  response = requests.get(url)

  # If the response works, extract and format the forecast data
  if response.ok:
    forecast_data = response.json()
    period = forecast_data["properties"]["periods"][0]
    return f"{relative_location} ({latitude:.2f}°N, {longitude:.2f}°W): {period['temperature']}F {period['temperatureTrend']} - {period['shortForecast']}"
    ## the degree symbols were copied from google docs 
  # If the response does not work, raise a red flag
  else:
    raise Exception('Your meteorologist has failed you.')

# Example usage with user input
latitude = float(input("Enter latitude: "))
longitude = float(input("Enter longitude: "))

forecast = get_grid_forecast(latitude, longitude)
if forecast:
  print(forecast)
else:
  print("Your meteorologist has failed you.")
