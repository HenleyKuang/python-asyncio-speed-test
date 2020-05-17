import asyncio
import logging
import time

from typing import List

LOGGER = logging.getLogger(__name__)


# Mock func for redis
async def hmget(cid: int, *fields):
    return [
        "1",
        "14",
        "www.google.com",
        "40.7127",
        "-74.0059",
        "Google",
        "US",
        "en",
    ]


async def run1(cid: int, fields: List[str]):
    values = await hmget(cid, *fields)
    # Create a dict of <se metadata name>: <se metadata value>
    results = dict(zip(fields, values))
    LOGGER.info(results)
    # Redis returns all values as str
    # Format metadata values to correct types
    if 'a' in results and results['a'] is not None:
        results['a'] = int(results['a'])
    if 'd' in results and results['d'] is not None:
        results['d'] = float(results['d'])
    if 'e' in results and results['e'] is not None:
        results['e'] = float(results['e'])
    if 'b' in results and results['b'] is not None:
        results['b'] = int(results['b'])
    if 'i' in results and results['i'] is not None:
        results['i'] = int(results['i'])
    if 'j' in results and results['j'] is not None:
        results['j'] = int(results['j'])
    if 'k' in results and results['k'] is not None:
        results['k'] = int(results['k'])
    return results

FEILDS_INT = set(['a', 'b', 'i', 'j', 'k'])
FIELDS_FLOAT = set(['d', 'e'])


async def convert(field, value):
    if value is not None and field in FEILDS_INT:
        return int(value)
    if value is not None and field in FIELDS_FLOAT:
        return float(value)
    return value


async def dict_zip_convert(fields, values):
    length = len(fields)
    rdict = {}
    for i in range(length):
        field = fields[i]
        value = await convert(field, values[i])
        rdict[field] = value
    return rdict


async def run2(cid: int, fields: List[str]):
    values = await hmget(cid, *fields)
    # Create a dict of <se metadata name>: <se metadata value>
    return await dict_zip_convert(fields, values)


async def main():
    cid = 34
    fields = ["a", "b", "c", "d", "e", "f", "g", "h"]
    data = await run2(cid, fields)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_time = time.time() * 1000
    loop = asyncio.get_event_loop()
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(main())
    loop.close()
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    LOGGER.info(elapsed_time)
