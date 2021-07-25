import configparser
import numpy as np
from zipfile import ZipFile

class Metadata():
    
    def __init__(self):
        self.config_main = configparser.ConfigParser()
        self.config_main.read('configuration.ini')

        self.config_device = configparser.ConfigParser()
        self.config_device.read(self.config_main['path']['ini_path'])

        # device configuration
        self.ini_path = self.config_main['path']['ini_path']
        self.save_path = self.config_main['path']['save_path']
        self.save_spectrum_path = ''
        self.save_spectrum_name = ''
        self.save_ratio_path = ''
        self.save_ratio_name = ''
        self.save_zip_path = ''


        self.position_count = int(self.config_device['position']['number'])
        self.position_default = self.position_count
        self.serial_device = ''
        self.serial_sample = ''
        self.measurement_data = np.empty((0,8000), np.double)
        self.ratio_data = np.empty((1, 8000), np.double)

        # 

    def update_metadata_config(self, config_input):
        self.serial_device = config_input["serial_device"]
        self.serial_sample = config_input["serial_sample"]
        self.save_spectrum_name = config_input["serial_sample"] + "_spectrum.txt"
        self.save_spectrum_path = self.save_path + self.save_spectrum_name
        self.save_ratio_name = config_input["serial_sample"] + "_ratio.txt"
        self.save_ratio_path = self.save_path + self.save_ratio_name
        self.save_zip_path = self.save_path + config_input["serial_sample"]  + self.serial_device + ".zip"


    def save_ratio(self):
        with open (self.save_ratio_path, 'w') as f:
            f.write('Ratio\n')
            for i in range(0, 8000):
                f.write(str(self.ratio_data[0][i]) + '\n')


    def save_zip(self):
        my_zipfile = ZipFile(self.save_zip_path, 'w')
        my_zipfile.write(self.save_spectrum_path)
        my_zipfile.write(self.save_ratio_path)
        my_zipfile.close()
