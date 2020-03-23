
class Ventilator(object):
    def __init__(self, spots):
        self.max_occupancy = spots
        self.occupants = set()

    @property
    def is_full(self):
        return len(self.occupants) == self.max_occupancy

    def add_patient(self, patient):
        self.occupants.add(patient)

    def remove_patient(self, patient):
        self.occupants.remove(patient)

    @property
    def average_ventilator_score(self):
        if self.occupants:
            return round(sum([pnt.ventilator_score for pnt in self.occupants]) / float(len(self.occupants)), 4)
        return 400
