import asyncio
import json

import websockets


async def producer_handler(websocket, path):
    while True:
        print("sending data")
        await websocket.send(json.dumps({"data": {"rpm": 1000}}))
        await asyncio.sleep(1)


async def setup(websocket):
    print("sending setup")
    a = {"rpm": {
        "max": 9000,
        "sectors": [
            {
                "color": "#d64d8a",
                "hi": 9000,
                "lo": 0
            }
        ],
        "tag": "bar1"
    }}
    await websocket.send(json.dumps({"setup": a}))


async def consumer_handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data["action"] == "setup":
            await setup(websocket)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()



start_server = websockets.serve(handler, "127.0.0.1", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()