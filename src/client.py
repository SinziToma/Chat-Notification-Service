import asyncio
import websockets

async def hello():
    uri = "ws://51.124.90.72:8765"
    async with websockets.connect(uri) as websocket:
        name = "1 2"

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        while greeting != None:
            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())