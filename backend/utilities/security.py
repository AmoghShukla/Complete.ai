from pwdlib import PasswordHash

from backend.utilities.exceptions import BadRequestException



password_context : PasswordHash = PasswordHash.recommended()

class Security:

    @staticmethod
    def hash_password(password : str):
        try:
            password_context.hash(password)
        except Exception as e:
            raise BadRequestException("Error while hashing the password")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            password_context.verify(plain_password, hashed_password)
        except Exception as e:
            raise BadRequestException("Error while Verifying the Password!!")