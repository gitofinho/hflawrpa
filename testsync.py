import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # 네트워크 요청을 시뮬레이션
    return {"data": 1}

async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)

async def main():
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_numbers())

    # 두 태스크가 완료될 때까지 기다립니다.
    data = await task1
    await task2
    print(data)

asyncio.run(main())
