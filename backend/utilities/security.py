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