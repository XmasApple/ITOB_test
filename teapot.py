import threading
import time

import logging
from logger import SQLiteHandler

import os
from dotenv import load_dotenv

load_dotenv()

STARTING_TEMP: float = float(os.getenv('STARTING_TEMP'))
MAX_TEMP: float = float(os.getenv('MAX_TEMP'))
TIME_TO_BOIL: float = float(os.getenv('TIME_TO_BOIL'))
MAX_WATER_LEVEL: float = float(os.getenv('MAX_WATER_LEVEL'))

LOGS_DB_PATH: str = os.getenv('LOGS_DB_PATH')


class Teapot:
    def __init__(self, time_to_boil: float = TIME_TO_BOIL, max_water_level: float = MAX_WATER_LEVEL):
        self.time_to_boil: float = time_to_boil
        self.max_water_level: float = max_water_level
        self.water_level: float = 0
        self.is_boiling: bool = False
        self.temp: float = 0
        self.start_temp: float = 0

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        logs_handler = SQLiteHandler(LOGS_DB_PATH)
        logs_handler.setLevel(logging.INFO)

        logging.getLogger().addHandler(logs_handler)
        logging.info('Teapot created')

    def set_water_level(self, water_level: float, water_temp: float) -> (bool, str):
        if self.is_boiling:
            msg = 'Teapot is on'
            logging.error(msg)
            return False, msg

        if water_level > self.max_water_level:
            msg = f'Water level is more than {self.max_water_level}'
            logging.error(msg)
            return False, msg

        if water_level <= 0:
            msg = 'Water level should be more than 0'
            logging.error(msg)
            return False, msg

        self.temp = water_temp
        self.start_temp = water_temp
        self.water_level = water_level

        msg = f'Water added, teapot temp is {self.temp}, water level is {self.water_level}'
        logging.info(msg)
        return True, msg

    def start_boiling(self) -> (bool, str):
        if self.water_level <= 0:
            msg = 'No water'
            logging.error(msg)
            return False, msg

        self.is_boiling = True
        threading.Thread(target=self._boil).start()
        msg = 'Boiling started'
        logging.info(msg)
        return True, msg

    def stop_boiling(self) -> (bool, str):
        self.is_boiling = False
        msg = 'Boiling stopped'
        logging.info(msg)
        return True, msg

    def _boil(self):
        temp_increase = (MAX_TEMP - self.start_temp) / self.time_to_boil
        while self.is_boiling:
            self.temp += temp_increase
            if self.temp >= MAX_TEMP:
                self.temp = MAX_TEMP
                self.is_boiling = False
                msg = f'Teapot temp is {self.temp}, boiling finished'
                logging.info(msg)
                print(msg)
                return
            msg = f'Teapot temp is {self.temp}, teapot is boiling'
            logging.info(msg)
            time.sleep(1)

    def __str__(self):
        return f'Teapot status: temp {self.temp}, ' \
               f'water level {self.water_level}, ' \
               f'{"boiling" if self.is_boiling else "not boiling"}'
