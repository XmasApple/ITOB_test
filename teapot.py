# Написать класс, который описывает электрический чайник с кнопкой включения и функцией автоматического выключения.
#
# - Количество воды задаётся числом с плавующей точкой от 0 до 1.0;
# - Время закипания - 10 секунд;
# - Выводить сообщения при смене состояния (вкл, выкл, вскипел, остановлен);
# - Если чайник включен, выводить температуру чайника каждую секунду;
# - В любой момент пользователь может нажать кнопку, чтобы отключить чайник, в этом случае, программа завершится;
import threading
import time

DEFAULT_TEMP: float = 20
DEFAULT_MAX_TEMP: float = 100
DEFAULT_TIME_TO_BOIL: float = 10
DEFAULT_MAX_WATER_LEVEL: float = 1.0


class Teapot:
    def __init__(self, time_to_boil: float = DEFAULT_TIME_TO_BOIL, max_water_level: float = DEFAULT_MAX_WATER_LEVEL):
        self.time_to_boil: float = time_to_boil
        self.max_water_level: float = max_water_level
        self.water_level: float = 0
        self.is_boiling: bool = False
        self.temp: float = 0
        self.start_temp: float = 0

    def set_water_level(self, water_level: float, water_temp: float) -> (bool, str):
        # can't add water if teapot is on
        if self.is_boiling:
            return False, 'Teapot is on'
        if water_level > self.max_water_level:
            return False, 'Too much water'

        self.temp = water_temp
        self.start_temp = water_temp
        self.water_level = water_level
        return True, f'Water added, teapot temp is {self.temp}, water level is {self.water_level}'

    def start_boiling(self) -> (bool, str):
        if self.water_level == 0:
            return False, 'No water'

        self.is_boiling = True
        threading.Thread(target=self._boil).start()
        return True, 'Teapot is on'

    def stop_boiling(self) -> (bool, str):
        self.is_boiling = False
        return True, 'Teapot is off'

    def _boil(self):
        # calculate temp increase per second
        temp_increase = (DEFAULT_MAX_TEMP - self.start_temp) / self.time_to_boil
        while self.is_boiling:
            # increase temp
            self.temp += temp_increase
            # if temp is more than max temp, set it to max temp
            if self.temp > DEFAULT_MAX_TEMP:
                self.temp = DEFAULT_MAX_TEMP
            # if temp is more than 100, stop boiling
            if self.temp >= DEFAULT_MAX_TEMP:
                self.is_boiling = False
                print(f'Teapot temp is {self.temp}, teapot is boiling')
                return
            print(f'Teapot temp is {self.temp}')
            time.sleep(1)

    def __str__(self):
        return f'Teapot status: temp {self.temp}, ' \
               f'water level {self.water_level}, ' \
               f'{"boiling" if self.is_boiling else "not boiling"}'
