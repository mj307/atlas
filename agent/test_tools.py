import asyncio
from agent.tools import calculate, convert_units, compute_stats


async def main():
    print("Testing calculate...")
    res1 = await calculate.ainvoke({"expression": "2 + 2"})
    print("calculate result:", res1)

    print("\nTesting convert_units...")
    res2 = await convert_units.ainvoke({
        "value": 1000,
        "from_unit": "m",
        "to_unit": "km"
    })
    print("convert result:", res2)

    print("\nTesting statistics...")
    res3 = await compute_stats.ainvoke({
        "numbers": [1, 2, 3, 4, 5]
    })
    print("stats result:", res3)


asyncio.run(main())