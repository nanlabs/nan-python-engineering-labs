"""
Async Rust functions with PyO3.
Demonstrates async/await patterns.
"""

import asyncio

async def async_fetch_data(delay: float) -> str:
    """Simulate async data fetch."""
    await asyncio.sleep(delay)
    return "Data fetched"

def run_async_function():
    """Helper to run async function."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_fetch_data(0.1))
        return result
    finally:
        loop.close()

if __name__ == "__main__":
    print("Async result:", run_async_function())
