import requests

class MGMWeather:
    def __init__(self, location):
        self.location = self.clear_tr_character(location)
        self.location_id = None
        self.latitude = None
        self.longitude = None
        self.current_degree = None

    def clear_tr_character(self, city_name):
        replacements = {
            "ı": "i", "ü": "u", "ğ": "g", "ş": "s", "ö": "o", "ç": "c"
        }
        for tr_char, lat_char in replacements.items():
            city_name = city_name.replace(tr_char, lat_char)
        return city_name.lower()

    def request(self, url):
        headers = {
            "Host": "servis.mgm.gov.tr",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "Origin": "https://www.mgm.gov.tr"
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def fetch_data(self):
        city_data_url = f"https://servis.mgm.gov.tr/web/merkezler?il={self.location}"
        city_data = self.request(city_data_url)
        self.location_id = city_data[0]["merkezId"]
        self.longitude = city_data[0]["boylam"]
        self.latitude = city_data[0]["enlem"]

        city_current_weather_url = f"https://servis.mgm.gov.tr/web/sondurumlar?merkezid={self.location_id}"
        city_current_weather = self.request(city_current_weather_url)
        self.current_degree = city_current_weather[0]["sicaklik"]

    def get_current_temperature(self):
        self.fetch_data()
        return self.current_degree


weather = MGMWeather("İzmir")
temperature = weather.get_current_temperature()
print(f"İzmir'in anlık sıcaklığı: {temperature}°C")
