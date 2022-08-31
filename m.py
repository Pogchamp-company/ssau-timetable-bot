import asyncio

from api import SsauAPI


async def main():
    api = SsauAPI()
    f = await api.get_timetable_by(755922237, 1)
    print(f)

if __name__ == '__main__':
    asyncio.run(main())
