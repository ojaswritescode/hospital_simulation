import unittest

from covid import patient, ventilator


class VentilatorTest(unittest.TestCase):
    
    def setUp(self):
        self.patients = []
        self._add_patients()

    def _add_patients(self):
        patient.Patient('m', 60)
        patient.Patient('m', 61)
        patient.Patient('m', 64)
        patient.Patient('m', 65)
        patient.Patient('m', 69)
        patient.Patient('m', 72)
        patient.Patient('m', 60)
        patient.Patient('f', 45)
        patient.Patient('f', 43)
        patient.Patient('f', 48)
        patient.Patient('f', 65)
        patient.Patient('f', 62)
        patient.Patient('m', 60)
        patient.Patient('f', 46)
        patient.Patient('m', 60)

    def test_stuff(self):
        pass
        # implement a test
