from PyQt5 import QtWidgets, uic
from numpy.core.fromnumeric import size
import model.signalgenerator as sg
import model.metadata as meta
import numpy as np

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)

        self.data = meta.Metadata()
        self.device = sg.Signalgenerator()

        # signal and slot
        self._in_bt_connect.clicked.connect(self.m_connect)
        self._in_bt_measure.clicked.connect(self.m_measure_all)
        self._in_bt_save.clicked.connect(self.m_save)
        self._in_bt_analyse.clicked.connect(self.m_analyse)
        self.show()


    def m_connect(self):
        # update metadata configuration
        gui_config = {"serial_sample": self._in_le_sample_sn.text(), "serial_device": self._in_le_device_sn.text()}
        self.data.update_metadata_config(gui_config)

        # configure signal generator
        self.device.set_filename(self.data.save_spectrum_path)
        self.device.configure_device(self.data.position_count)

        self._in_pte_log.appendPlainText("Set position 1 and start measurement:")


    def m_measure(self):
        self.device.measure_signal()


    def m_save(self):
        self.device.save_signal()
        self.data.save_ratio()
        self.data.save_zip()
        self._in_pte_log.appendPlainText("Data has been saved.")


    def m_measure_all(self):
        if self.data.position_count > 0:
            index = self.data.position_default - self.data.position_count + 1

            self.device.measure_signal()

            self.data.position_count -= 1
            self.data.measurement_data = np.append(self.data.measurement_data,
                np.array([self.device.get_signal()]), axis=0)

            self._in_pte_log.appendPlainText("Measurement: {} is done.".format(index))
            if index < self.data.position_default:
                self._in_pte_log.appendPlainText("Set Position: {} and start measurement:".format(index+1))
        else:
            self._in_pte_log.appendPlainText("Measurements are finished.")



    def m_analyse(self):
        ratio_data = np.empty(8000)
        for i in range(0, 8000):
            ratio_data[i] = self.data.measurement_data[0][i] / self.data.measurement_data[1][i]

        self.data.ratio_data = np.array([ratio_data])       
        self._in_pte_log.appendPlainText("Analyse is finished.")

