import keyboard

from teapot import Teapot


def read_float(prompt: str,
               min_val: float | None = None,
               max_val: float | None = None,
               default: float | None = None,
               ) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f'Value must be in range {min_val} - {max_val}')
            elif max_val is not None and value > max_val:
                print(f'Value must be in range {min_val} - {max_val}')
            else:
                return value
        except ValueError:
            if default is not None:
                return default
            else:
                print('Please enter a float')


def read_fill_params() -> (float, float):
    water_level: float = read_float('Enter water level: ', min_val=0, max_val=1)
    water_temp: float = read_float(
        'Enter water temp: ', min_val=0, max_val=100, default=20)
    return water_level, water_temp


def main():
    teapot = Teapot()
    water_level, water_temp = read_fill_params()
    teapot.set_water_level(water_level, water_temp)

    print(teapot)

    input('Press "Enter" to start boiling')
    teapot.start_boiling()
    print('Boiling started')
    print('press "q" to stop boiling')

    while teapot.is_boiling:
        if keyboard.is_pressed('q'):
            teapot.stop_boiling()
            print('Boiling stopped')
            break


if __name__ == '__main__':
    main()
