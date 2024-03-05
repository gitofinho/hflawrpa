import requests

BASE_URL = "http://localhost:9090"

def create_user(name, email):
    response = requests.post(f"{BASE_URL}/users/", json={"name": name, "email": email})
    if response.status_code == 201:
        print("User created successfully:", response.json())
    else:
        print("Failed to create user:", response.status_code)

def get_users():
    response = requests.get(f"{BASE_URL}/users/")
    if response.ok:
        print("User list:", response.json())
    else:
        print("Failed to get users:", response.status_code)

def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.ok:
        print("User details:", response.json())
    else:
        print("Failed to get user:", response.status_code)

def update_user(user_id, name, email):
    response = requests.put(f"{BASE_URL}/users/{user_id}", json={"name": name, "email": email})
    if response.ok:
        print("User updated successfully:", response.json())
    else:
        print("Failed to update user:", response.status_code)

def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 204:
        print("User deleted successfully")
    else:
        print("Failed to delete user:", response.status_code)

import random
import time

# 예제 사용
try:
    # 일정 횟수의 사용자 생성을 위해 while 대신 for 루프 사용
    for _ in range(1000):  # 예를 들어 10명의 사용자를 생성
        start_time = time.time()  # 시작 시간 측정
        create_user("John Updated", f"{random.randint(1,100000)}johnupdated@example.com")
        end_time = time.time()  # 종료 시간 측정
        lapse = end_time - start_time  # 실행 시간 계산
        print(f"User created in {lapse} seconds.")

except KeyboardInterrupt:
    print("Process interrupted.")