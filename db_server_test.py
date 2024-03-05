from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiosqlite

app = FastAPI()
DATABASE_URL = "sqlite_async.db"

class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str

@app.on_event("startup")
async def startup():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        await db.commit()

# 사용자 목록 조회
@app.get("/users/", response_model=list[User])
async def read_users():
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("SELECT id, name, email FROM users")
        users = await cursor.fetchall()
        return [User(id=row[0], name=row[1], email=row[2]) for row in users]

# 특정 사용자 조회
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(id=row[0], name=row[1], email=row[2])

# 새로운 사용자 추가
@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
        await db.commit()
        new_user_id = cursor.lastrowid
        return {**user.dict(), "id": new_user_id}

# 사용자 정보 업데이트
@app.put("/users/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (user.name, user.email, user_id))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return user

# 사용자 삭제
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
