import bcrypt

def get_password_hash(password: str) -> str:
    """
    Генерация хэша пароля
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())