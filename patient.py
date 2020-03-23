import uuid

MALE = 'm'
FEMALE = 'f'
NONBINARY = 'x'
VENTILATOR_CONSTANT = 2.3


class Patient(object):
    def __init__(self, gender, height):
        self.patient_id = 'P' + str(uuid.uuid4().int)[:7]  # unique identifier for patient
        self.gender = gender  # 'm' or 'f'
        self.height = height  # int inches
        self.ventilator_number = None

    def __repr__(self):
        return str((self.patient_id, self.ventilator_score, self.ventilator_number))

    @property
    def ventilator_score(self):
        if self.gender == MALE:
            score = 50
        else:
            score = 45.5
        score += VENTILATOR_CONSTANT * (self.height - 60)
        score *= 8
        return round(score, 4)

    @property
    def is_assigned(self):
        return bool(self.ventilator_number)

