from pwdlib import PasswordHash



password_context : PasswordHash = PasswordHash.recommended()

class Security:

    @staticmethod
    def hash_password() 