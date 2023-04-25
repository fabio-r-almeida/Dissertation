import configparser
class config_ini_parser():
    def __init__(self):
        pass
    def set_module(self, data):
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            converted = "{"
            for key in data:
                converted += '\"' + key + '\"' + ": \"" + str(data[key]) + '\",'
            converted = converted[:-1]
            converted += "}"
            parser.set('MODULE', 'module', converted)
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)

    def set_inverter(self, data):
            import json
            data = data.to_json(orient="records")
            data = data[1:]
            data = data[:-1]
            data = data.replace("%","%%")
            data = json.loads(data)
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            converted = "{"
            for key in data:
                converted += '\"' + key + '\"' + ": \"" + str(data[key]) + '\",'
            converted = converted[:-1]
            converted += "}"
            parser.set('INVERTER', 'inverter', converted)
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)

    def set_location(self, latitude, longitude):
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            parser.set('LOCATION', 'latitude', str(latitude))
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)
            parser.set('LOCATION', 'longitude', str(longitude))
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)

    def set_checkbox_power(self, power):
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            parser.set('SIMULATE', 'power', str(power))
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)

    def set_checkbox_ppfd(self, ppfd):
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            parser.set('SIMULATE', 'ppfd', str(ppfd))
            with open("config.ini", "w+") as configfile:
                parser.write(configfile)