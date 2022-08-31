import asyncio

from api import SsauAPI


async def main():
    api = SsauAPI()
    f = await api.get_institutes_and_faculties()
    print(len(f), f)

if __name__ == '__main__':
    asyncio.run(main())
