import logging as log
from typing import Optional

from fastapi import FastAPI, HTTPException
from yeelight import discover_bulbs
from yeelight.aio import AsyncBulb
from pydantic import BaseModel

log.basicConfig(level=log.INFO)
app = FastAPI()
bulbs_obj = {}
bulbs_names = {}


class RgbValue(BaseModel):
    red: Optional[int] = 0
    green: Optional[int] = 0
    blue: Optional[int] = 0


def get_callback_handler(ip: str, b_id: int):
    def my_callback(data):
        log.info(f"bulb: {b_id} ({ip}):  {data}")
    return my_callback


def get_bulb(bulb_id: int):
    try:
        return bulbs_obj[bulb_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


async def discover_and_connect():
    bulbs = discover_bulbs()
    for idx, bulb in enumerate(bulbs):
        bulb_ip = bulb["ip"]
        bulbs_obj[idx] = AsyncBulb(bulb_ip)
        await bulbs_obj[idx].async_listen(get_callback_handler(bulb_ip, idx))
        bulbs_names[idx] = bulb["capabilities"]["name"]
    return bulbs


@app.get("/bulbs")
async def handle_discover():
    return [{"id": bulb_id,
             "name": bulbs_names[bulb_id]}
            for bulb_id in bulbs_obj.keys()]


@app.put("/{bulb_id}/turn_off")
async def handle_turn_off(bulb_id: int):
    await get_bulb(bulb_id).async_turn_off()
    return {"status": "ok"}


@app.put("/{bulb_id}/turn_on")
async def handle_turn_on(bulb_id: int):
    await get_bulb(bulb_id).async_turn_on()
    return {"status": "ok"}


@app.put("/{bulb_id}/rgb")
async def handle_handle_set_rgb(bulb_id: int, item: RgbValue):
    await get_bulb(bulb_id).async_set_rgb(item.red, item.green, item.blue)
    return {"status": "ok"}


@app.put("/{bulb_id}/brightness")
async def handle_set_brightness(bulb_id: int, value: int):
    await get_bulb(bulb_id).async_set_brightness(value)
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    await discover_and_connect()


@app.on_event("shutdown")
async def shutdown_event():
    for bulb in bulbs_obj.values():
        await bulb.async_stop_listening()
    log.info("Application shutdown")
