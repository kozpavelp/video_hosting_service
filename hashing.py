from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_pwd(password, hashed):
        return password_context.verify(password, hashed)

    @staticmethod
    def get_pwd_hash(password: str) -> str:
        return password_context.hash(password)
