import nest
from nest import utils as nest_utils

from util import delay


class Nester:
    def __init__(self, cfg=None):
        if (cfg is None):
            print("No username/password provided for Nest")
            return
        self.napi = nest.Nest(cfg.nest_username, cfg.nest_password)
        try:
            self.structure = self.napi.structures[0]
            self.device = self.structure.devices[0]
        except:
            print("Could Not find a nest device, it's all over")
            return

        self.current_temp = nest_utils.c_to_f(self.device.temperature)
        self.outside_temp = nest_utils.c_to_f(self.device.temperature)
        self.debug()

    def colder(self):
        print("old target ", nest_utils.c_to_f(self.device.target))
        self.device.target -= 1
        print("new target ", nest_utils.c_to_f(self.device.target))

    def hotter(self):
        print("old target ", nest_utils.c_to_f(self.device.target))
        self.device.target += 1
        print("new target ", nest_utils.c_to_f(self.device.target))

    def fan_off(self):
        self.device.fan = False

    def fan_on(self):
        print("turn on that fan, i can't breath!")
        self.device.fan = True
        delay(lambda: self.fan_off(), delay=600)

    @property
    def inside_temperature(self):
        return round(nest_utils.c_to_f(self.device.temperature))

    @property
    def outside_temperature(self):
        return round(nest_utils.c_to_f(self.structure.weather.current.temperature))

    @property
    def target(self):
        return round(nest_utils.c_to_f(self.device.target))

    def debug(self):
        for structure in self.napi.structures:
            print('Structure %s' % structure.name)
            print('    Away: %s' % structure.away)
            print('    Devices:')

            for device in structure.devices:
                print('        Device: %s' % device.name)
                print('            Temp: %0.1f' % device.temperature)

        # Access advanced structure properties:
        for structure in self.napi.structures:
            print('Structure   : %s' % structure.name)
            print(' Postal Code                    : %s' % structure.postal_code)
            print(' Country                        : %s' % structure.country_code)
            print(' dr_reminder_enabled            : %s' % structure.dr_reminder_enabled)
            print(' eta_preconditioning_active     : %s' % structure.eta_preconditioning_active)
            print(' house_type                     : %s' % structure.house_type)
            print(' hvac_safety_shutoff_enabled    : %s' % structure.hvac_safety_shutoff_enabled)
            print(' num_thermostats                : %s' % structure.num_thermostats)
            # print(' measurement_scale              : %s' % structure.measurement_scale)
            print(' renovation_date                : %s' % structure.renovation_date)
            print(' structure_area                 : %s' % structure.structure_area)

            # Access advanced device properties:
            for device in structure.devices:
                print('        Device: %s' % device.name)
            print('        Where: %s' % device.where)
            print('            Mode     : %s' % device.mode)
            print('            Fan      : %s' % device.fan)
            print('            Temp     : %0.1fC' % device.temperature)
            print('            Humidity : %0.1f%%' % device.humidity)
            #print('            Target   : %0.1fC' % device.target)
            print('            Away Heat: %0.1fC' % device.away_temperature[0])
            print('            Away Cool: %0.1fC' % device.away_temperature[1])
            # print('            Eco      : %s' % device.eco)

            print('            hvac_ac_state         : %s' % device.hvac_ac_state)
            print('            hvac_cool_x2_state    : %s' % device.hvac_cool_x2_state)
            print('            hvac_heater_state     : %s' % device.hvac_heater_state)
            print('            hvac_aux_heater_state : %s' % device.hvac_aux_heater_state)
            print('            hvac_heat_x2_state    : %s' % device.hvac_heat_x2_state)
            print('            hvac_heat_x3_state    : %s' % device.hvac_heat_x3_state)
            print('            hvac_alt_heat_state   : %s' % device.hvac_alt_heat_state)
            print('            hvac_alt_heat_x2_state: %s' % device.hvac_alt_heat_x2_state)
            print('            hvac_emer_heat_state  : %s' % device.hvac_emer_heat_state)

            print('            online                : %s' % device.online)
            print('            last_ip               : %s' % device.last_ip)
            print('            local_ip              : %s' % device.local_ip)
            print('            last_connection       : %s' % device.last_connection)

            print('            error_code            : %s' % device.error_code)
            print('            battery_level         : %s' % device.battery_level)

            # Weather data is also available under structure or device
            # The api is the same from either

            structure = self.napi.structures[0]
            time_str = structure.weather.current.datetime.strftime('%Y-%m-%d %H:%M:%S')
            print('Current Weather at %s:' % time_str)
            print('    Condition: %s' % structure.weather.current.condition)
            print('    Temperature: %s' % structure.weather.current.temperature)
            print('    Humidity: %s' % structure.weather.current.humidity)
            # print('    Wind Dir: %s' % structure.weather.current.wind.direction)
            # print('    Wind Azimuth: %s' % structure.weather.current.wind.azimuth)
            print('    Wind Speed: %s' % structure.weather.current.wind.kph)

            # NOTE: Hourly forecasts do not contain a "contidion" its value is `None`
            #       Wind Speed is likwise `None` as its generally not reported
            print('Hourly Forcast:')
            for f in structure.weather.hourly:
                print('    %s:' % f.datetime.strftime('%Y-%m-%d %H:%M:%S'))
                print('        Temperature: %s' % f.temperature)
                print('        Humidity: %s' % f.humidity)
                # print('        Wind Dir: %s' % f.wind.direction)
                # print('        Wind Azimuth: %s' % f.wind.azimuth)

            # NOTE: Daily forecasts temperature is a tuple of (low, high)
            print('Daily Forcast:')
            for f in structure.weather.daily:
                print('    %s:' % f.datetime.strftime('%Y-%m-%d %H:%M:%S'))
                print('    Condition: %s' % structure.weather.current.condition)
                print('        Low: %s' % f.temperature[0])
                print('        High: %s' % f.temperature[1])
                print('        Humidity: %s' % f.humidity)
                # print('        Wind Dir: %s' % f.wind.direction)
                # print('        Wind Azimuth: %s' % f.wind.azimuth)
                print('        Wind Speed: %s' % structure.weather.current.wind.kph)
