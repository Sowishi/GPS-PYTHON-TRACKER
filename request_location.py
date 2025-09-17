import asyncio
from obdtracker import api, location

async def main(device_id, password):
    ai = api.API("https://en.aika168.com/")  # or whatever base URL the library expects
    # For some devices you might need to do something like ai.doLogin(device_id, password)
    await ai.doLogin(device_id, password)
    loc = await location.Location(ai).getTracking()
    print("Current Location:", loc)

if __name__ == "__main__":
    # replace with your device id & password
    asyncio.run(main("9176502935", "123456"))
