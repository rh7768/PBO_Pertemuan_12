from abc import ABC, abstractmethod


class Student:
    """Representasi data mahasiswa."""

    def __init__(self, sks, has_prerequisite):
        """
        Args:
            sks (int): Jumlah SKS yang diambil.
            has_prerequisite (bool): Status prasyarat.
        """
        self.sks = sks
        self.has_prerequisite = has_prerequisite


class Validator(ABC):
    """Interface untuk aturan validasi."""

    @abstractmethod
    def validate(self, student):
        """
        Args:
            student (Student): Objek mahasiswa.

        Returns:
            tuple: (bool, str) hasil validasi dan pesan.
        """
        pass


class SKSValidator(Validator):
    """Validasi batas maksimal SKS."""

    def validate(self, student):
        if student.sks > 24:
            return False, "SKS melebihi batas"
        return True, ""


class PrerequisiteValidator(Validator):
    """Validasi prasyarat mata kuliah."""

    def validate(self, student):
        if not student.has_prerequisite:
            return False, "Prasyarat belum terpenuhi"
        return True, ""


class ValidatorManager:
    """Mengelola proses validasi registrasi."""

    def __init__(self, validators):
        """
        Args:
            validators (list): Daftar validator.
        """
        self.validators = validators

    def validate(self, student):
        """
        Args:
            student (Student): Mahasiswa yang divalidasi.

        Returns:
            str: Hasil validasi.
        """
        for validator in self.validators:
            valid, message = validator.validate(student)
            if not valid:
                return message
        return "Registrasi berhasil"
