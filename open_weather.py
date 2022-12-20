import requests
# from os import getenv
# from dotenv import load_dotenv

# load_dotenv() # будет искать файл .env, и, если он его найдет, из него будут загружены переменные среды
from dotenv import dotenv_values
config = dotenv_values(".env")


class Weather(object):
    """_summary_

    Returns:
        _type_: _description_

    Dependence: requests
    """

    __APIKEY = config.get("APIID")

    def __init__(self, lang: str='ru') -> str:
        self.lang = lang

    def get_local_name(self, response: dict) -> str:
        try:
            name = response['local_names'][self.lang]
        except:
            name = response['name']
        return name

    def get_coordintes(self, city: str) -> list:
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.__APIKEY}")
        if response.status_code == 200:
            response = response.json()[0]
            name = self.get_local_name(response)
            return response['lat'], response['lon'], name
        return 'Try again'

    def get_weather(self, city: str) -> list:
        temp = self.get_coordintes(city)
        lat, lon, name = temp
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&"
                                f"lang={self.lang}&appid={self.__APIKEY}")
        if response.status_code == 200:
            response = response.json()
            weather = response['weather'][0]['description']
            temperature = response['main']['temp']
            country = response['sys']['country']
            return name, country, weather, temperature
        return 'Try again'

    def check_weather(self, *cities) -> str:
        # print(cities)
        result = []
        if len(cities) == 1:
            # print(type(cities[0]))
            if type(cities[0]) == str:
                # print('строка')
                cities = cities[0].split()
            elif type(cities[0]) == tuple:
                cities = cities[0]
                # print('кортеж')
        # print(cities)
        for city in cities:
            try:
                local_name, country, weather, temperature = self.get_weather(city)
                result.append(f"{local_name}, {country}: {temperature:.2f}\u00B0C {weather}")
            except IndexError:
                print(f'Города {city} не найдены')
        return result


weather = Weather()
a = 'санкт-петербург, владивосток, москва'
b = "волгоград", "саратов", "воронеж"
c = 'ростов-на-дону тверь орел'
d = ["кисловодск", "пятигорск", "белгород"]
print(*weather.check_weather(b), sep="\n")
