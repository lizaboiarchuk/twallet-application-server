import aiohttp

MONOBANK_URI = "https://api.monobank.ua/"


async def get_currency():
    async with aiohttp.ClientSession() as session:
        async with session.get(MONOBANK_URI + "bank/currency") as resp:
            result = await resp.json()
            return result
