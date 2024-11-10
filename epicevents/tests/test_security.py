from utils.security import hash_password, verify_password

def test_hash_password():
    password = "password123"
    hashed_password = hash_password(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)
    