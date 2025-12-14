from abc import ABC, abstractmethod


class Student:
    def __init__(self, sks, has_prerequisite):
        self.sks = sks
        self.has_prerequisite = has_prerequisite


class Validator(ABC):
    @abstractmethod
    def validate(self, student):
        pass


class SKSValidator(Validator):
    def validate(self, student):
        if student.sks > 24:
            return False, "SKS melebihi batas"
        return True, ""


class PrerequisiteValidator(Validator):
    def validate(self, student):
        if not student.has_prerequisite:
            return False, "Prasyarat belum terpenuhi"
        return True, ""


class ValidatorManager:
    def __init__(self, validators):
        self.validators = validators

    def validate(self, student):
        for validator in self.validators:
            valid, message = validator.validate(student)
            if not valid:
                return message
        return "Registrasi berhasil"


if __name__ == "__main__":
    student = Student(22, True)
    validators = [SKSValidator(), PrerequisiteValidator()]
    manager = ValidatorManager(validators)
    print(manager.validate(student))
