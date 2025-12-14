import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

LOGGER = logging.getLogger("Registration")


class Student:
    """Representasi data mahasiswa."""

    def __init__(self, sks, has_prerequisite):
        self.sks = sks
        self.has_prerequisite = has_prerequisite


class Validator(ABC):
    """Interface aturan validasi."""

    @abstractmethod
    def validate(self, student):
        pass


class SKSValidator(Validator):
    """Validasi batas SKS."""

    def validate(self, student):
        LOGGER.info("Validasi SKS mahasiswa")
        if student.sks > 24:
            LOGGER.warning("SKS melebihi batas")
            return False, "SKS melebihi batas"
        return True, ""


class PrerequisiteValidator(Validator):
    """Validasi prasyarat."""

    def validate(self, student):
        LOGGER.info("Validasi prasyarat mahasiswa")
        if not student.has_prerequisite:
            LOGGER.warning("Prasyarat belum terpenuhi")
            return False, "Prasyarat belum terpenuhi"
        return True, ""


class ValidatorManager:
    """Service validasi registrasi."""

    def __init__(self, validators):
        self.validators = validators

    def validate(self, student):
        LOGGER.info("Memulai proses registrasi")
        for validator in self.validators:
            valid, message = validator.validate(student)
            if not valid:
                LOGGER.error("Registrasi gagal")
                return message
        LOGGER.info("Registrasi berhasil")
        return "Registrasi berhasil"


if __name__ == "__main__":
    student = Student(22, True)
    validators = [SKSValidator(), PrerequisiteValidator()]
    manager = ValidatorManager(validators)
    print(manager.validate(student))
