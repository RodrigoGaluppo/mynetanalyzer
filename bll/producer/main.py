# main.py

import asyncio
from websockets.server import serve
from controllers.Host import host
from Global import server_ip, server_port

async def main():
    async with serve(host, server_ip, server_port):
        try:
            print("Waiting for host connections")
            await asyncio.Future()
        except Exception as err:
            print(err)
            pass

if __name__ == "__main__":
    asyncio.run(main())
