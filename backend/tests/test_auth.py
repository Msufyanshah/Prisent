import httpx
import sys

def run_tests():
    client = httpx.Client(base_url="http://localhost:8000")

    # Use a unique email for every test run
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_{unique_id}@prisent.ai"

    # Test 1: Register new user
    print("Test 1: Register new user...")
    reg_data = {"email": email, "password": "Test1234!", "name": "Test User"}
    r = client.post("/auth/register", json=reg_data)
    print("Reg status:", r.status_code)
    print("Reg response:", r.json())
    assert r.status_code == 201
    res = r.json()
    assert res["success"] is True
    assert res["error"] is None
    assert "timestamp" in res
    
    data = res["data"]
    assert "user_id" in data
    assert "token" in data
    assert data["name"] == "Test User"
    print("Test 1 PASS")

    # Test 2: Duplicate email is rejected
    print("\nTest 2: Register duplicate email...")
    r = client.post("/auth/register", json=reg_data)
    print("Dup status:", r.status_code)
    print("Dup response:", r.json())
    assert r.status_code == 400
    res = r.json()
    assert res["success"] is False
    assert res["data"] is None
    assert res["error"]["code"] == "EMAIL_TAKEN"
    print("Test 2 PASS")

    # Test 3: Login works
    print("\nTest 3: Login user...")
    login_data = {"email": email, "password": "Test1234!"}
    r = client.post("/auth/login", json=login_data)
    print("Login status:", r.status_code)
    print("Login response:", r.json())
    assert r.status_code == 200
    res = r.json()
    assert res["success"] is True
    assert res["data"]["token"] is not None
    print("Test 3 PASS")

    # Test 4: Wrong password is rejected
    print("\nTest 4: Login wrong password...")
    wrong_login_data = {"email": email, "password": "wrongpassword"}
    r = client.post("/auth/login", json=wrong_login_data)
    print("Wrong login status:", r.status_code)
    print("Wrong login response:", r.json())
    assert r.status_code == 401
    res = r.json()
    assert res["success"] is False
    assert res["error"]["code"] == "INVALID_CREDENTIALS"
    print("Test 4 PASS")

    print("\nALL 4 AUTH SMOKE TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
