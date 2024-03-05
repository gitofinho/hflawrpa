from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import aiosqlite

app = FastAPI()
DATABASE_URL = "sqlite_async.db"

class User(BaseModel):
    id: int = None  # 생성 시 id는 None이 될 수 있음
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str

# 데이터베이스 연결 에러 처리를 위한 커스텀 예외 핸들러
@app.exception_handler(aiosqlite.Error)
async def sqlite_exception_handler(request: Request, exc: aiosqlite.Error):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error: Database operation failed."},
    )

# Pydantic 유효성 검사 에러 처리
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Error: Invalid data.", "errors": exc.errors()},
    )

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

@app.get("/users/", response_model=list[User])
async def read_users():
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("SELECT id, name, email FROM users")
        users = await cursor.fetchall()
        return [User(id=row['id'], name=row['name'], email=row['email']) for row in users]

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(id=row['id'], name=row['name'], email=row['email'])

@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
        await db.commit()
        new_user_id = cursor.lastrowid
        return {**user.dict(), "id": new_user_id}

@app.put("/users/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (user.name, user.email, user_id))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    async with aiosqlite.connect(DATABASE_URL) as db:
        cursor = await db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
