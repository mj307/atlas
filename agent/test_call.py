import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8002/tools/calculate",
            headers={
                "Authorization": "Bearer mysecret123",
                "Content-Type": "application/json"
            },
            json={"expression": "6*6"}
        )

        print(response.json())

asyncio.run(test())