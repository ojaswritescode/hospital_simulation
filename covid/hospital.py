import itertools
import patient, ventilator


class ICUSimulation(object):

    def __init__(self, ventilator_count, ventilator_occupancy):
        self.patients = {}
        self.ventilators = {
            i: ventilator.Ventilator(ventilator_occupancy) for i in range(1, ventilator_count+1)
        }

    def add_patient(self):
        gender = raw_input('\nEnter patient gender (m/f/x) -- ')
        height = input('Enter patient height (inches) -- ')
        new_patient = patient.Patient(gender, height)
        print 'Patient with ID {} and ventilator score {} created'.format(
            new_patient.patient_id,
            new_patient.ventilator_score
        )
        self.patients[new_patient.patient_id] = new_patient
        print 'Patient is currently unassigned.'
        return new_patient

    def _assign_patient_to_ventilator(self, ventilator_id, pnt):
        pnt.ventilator_number = ventilator_id
        self.ventilators[ventilator_id].add_patient(pnt)

    def _remove_patient_from_ventilator(self):
        patient_id = raw_input('\nWhat patient ID would you like to unassign from a ventilator? -- ')
        vent_number = self.patients[patient_id].ventilator_number
        self.patients[patient_id].ventilator_number = None
        self.ventilators[vent_number].remove_patient(self.patients[patient_id])
        print 'Patient {} has been unassigned from ventilator {}\n'.format(patient_id, vent_number)

        remove_from_simulation = raw_input('Remove {} from the hospital simulation? (y/n)  -- '.format(patient_id))
        if remove_from_simulation == 'y':
            del self.patients[patient_id]
            print 'Patient {} removed from simulation\n'.format(patient_id)

    def get_open_ventilators(self):
        return [v_id for v_id, vent in self.ventilators.items() if not vent.is_full]

    def get_unassigned_patients(self):
        return [pnt for pnt in self.patients if not pnt.is_assigned]

    def _sort_patients(self):
        return sorted(self.patients.values(), key=lambda pnt: pnt.ventilator_score)
    
    def get_ventilators_and_patients(self):
        print '\nCurrent ventilator arrangement'
        for v_id, vent in self.ventilators.items():
            print 'Ventilator {} -- average tidal volume: {}'.format(v_id, vent.average_ventilator_score)
            for i, pnt in itertools.izip_longest(range(1, vent.max_occupancy+1), vent.occupants):
                print 'Spot {}: {}'.format(i, pnt or '')
            print '\n'

    def arrange_patients_on_ventilators(self):
        for v_id, vent in self.ventilators.items():
            for pnt in self._sort_patients():
                if not vent.is_full and not pnt.ventilator_number:
                    self._assign_patient_to_ventilator(v_id, pnt)

    def add_patient_dynamically(self, pnt):
        ventilator_averages = {
            v_id: vent.average_ventilator_score
            for v_id, vent in self.ventilators.items() if not vent.is_full
        }
        difference_from_averages = {
            v_id: abs(pnt.ventilator_score - avg)
            for v_id, avg in ventilator_averages.items()
        }
        minimum_ventilator_id = sorted(difference_from_averages.items(), key=lambda (k, v): v)[0][0]
        self._assign_patient_to_ventilator(minimum_ventilator_id, pnt)

    def create_and_add_patient_dynamic(self):
        print 'Adding patient dynamically'
        new_patient = self.add_patient()
        self.add_patient_dynamically(new_patient)

        if new_patient.ventilator_number:
            print 'Patient added to ventilator {}'.format(new_patient.ventilator_number)
        else:
            print 'No ventilators available\n'

    def create_and_add_patient_specific(self):
        print 'Adding patient to specific ventilator'
        new_patient = self.add_patient()
        ventilator_id = input('Specify ventilator for patient {}'.format(new_patient.patient_id))
        self._assign_patient_to_ventilator(ventilator_id, new_patient)

        if new_patient.ventilator_number:
            print 'Patient added to ventilator {}'.format(new_patient.ventilator_number)
        else:
            print 'No ventilators available\n'


    def list_all_patients_sorted_by_ventilator_score(self):
        for pnt in self._sort_patients():
            print pnt

    def menu(self):
        MENU_ITEMS = {
            1: ('Get current ventilator arrangement', self.get_ventilators_and_patients),
            2: ('Add patient to hospital (dynamical ventilator allocation)', self.create_and_add_patient_dynamic),
            3: ('Add patient to hospital (manual ventilator choice)', self.create_and_add_patient_specific),
            4: ('Remove patient from ventilator', self._remove_patient_from_ventilator),
            5: ('List all patients sorted by ventilator score', self.list_all_patients_sorted_by_ventilator_score),
        }
        for i, item in MENU_ITEMS.items():
            print '{} : {}'.format(i, item[0])
        choice = input('What would you like to do? -- ')
        MENU_ITEMS[choice][1]()


def run():
    ventilator_count = input('How many ventilators in your hospital? -- ')
    patients_per_ventilator = input('How many patients per ventilator? -- ')

    print 'Starting simulation...'

    hospital = ICUSimulation(ventilator_count, patients_per_ventilator)
    print 'Current open ventilators {}'.format(str(hospital.get_open_ventilators()))
    test_patients = []
    # test_patients = [
    #     patient.Patient('m', 60),
    #     patient.Patient('m', 61),
    #     patient.Patient('m', 64),
    #     patient.Patient('m', 65),
    #     patient.Patient('m', 69),
    #     patient.Patient('m', 72),
    #     patient.Patient('m', 60),
    #     patient.Patient('f', 45),
    #     patient.Patient('f', 43),
    #     patient.Patient('f', 48),
    #     patient.Patient('f', 65),
    #     patient.Patient('f', 62),
    #     patient.Patient('m', 60),
    #     patient.Patient('f', 46),
    #     patient.Patient('m', 60)
    # ]
    for pnt in test_patients:
        hospital.add_patient(pnt)

    print 'Your hospital has been created with {} patients already needing ventilation '.format(len(test_patients)
    )  
    hospital.arrange_patients_on_ventilators()
    hospital.get_ventilators_and_patients()

    while True:
        hospital.menu()


if __name__ == '__main__':
    run()
