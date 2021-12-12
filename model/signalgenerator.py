import random
import numpy as np
import time

class Signalgenerator():
    def __init__(self):
        self.Fs = 8000
        self.f = 2
        self.sample = 8000
        self.x = np.arange(1, self.sample+1)
        self.y = np.empty(self.sample)
        self.level = 0
        self.filename = ''


    def set_filename(self, name):
        self.filename = name


    def configure_device(self, level):
        self.level = level


    def measure_signal(self):
        for i in range(0, self.sample):
            delta = random.randint(1, self.level * 10) / 10 - self.level
            self.y[i] = self.level * 10 * np.cos(2* np.pi * self.f * i / self.Fs) + delta


    def get_signal(self):
        return self.y
    
    
    def save_signal(self):
        with open (self.filename, 'w') as f:
            f.write('Time=' + str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('Intensity=' + str(random.randint(1, self.level * 10)) + '\n')
            f.write('Spectrum:\n')
            for i in range(0, self.sample):
                f.write(str(self.x[i]) + '\t' +  str(self.y[i]) + '\n')