# This is a sample Python script.
import asyncio
import os
import json

import aiohttp
from aiohttp import web

import pymongo

WEBSOCKET_URL = "ws://websocket:8080"
#HOST = os.getenv('HOST', 'localhost')
#PORT = int(os.getenv('PORT', 1234))
PAGE_SIZE = 50
HOST = '0.0.0.0'
PORT = '1234'


client = pymongo.MongoClient('mongodb', 27017)
vehicle_collection = client['vehicle_database']['vehicles']


def write_to_database(db_collection: pymongo.collection.Collection, message: aiohttp.WSMessage):
    """
    Writes an object into Mongo database collection based on websocket message text

    :param db_collection: instance of mongo db collection
    :param message: a string which represents JSON-like object
    :return: None
    """
    try:
        json_msg = json.loads(message.data)
    except ValueError:
        return
    if not json_msg['country']:
        json_msg['country'] = 'USA'
    inserted_object = db_collection.insert_one(json_msg)


async def read_from_websocket(websocket_url: str):
    """
    Listen to a websocket available via websocket_url and send data to database

    :param websocket_url: websocket URL, ee.g. ws://172.17.0.2:8080
    :return: None
    """
    session = aiohttp.ClientSession()
    async with session.ws_connect(websocket_url) as ws:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                write_to_database(vehicle_collection, msg)
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                break


async def send_data_from_db(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """
    Reads data from collection and returns Responobject with total number of documents, page number and
    paginated set of json objects. A page size is set via PAGE_SIZE.
    Page number can be provided via 'page' argument of HTTP request, e.g. 'http://0.0.0.0:8080/?page=3'

    :param request: aiohttp HTTP request ws://172.17.0.2:8080"
    :return: aiohttp web HTTP response object
    """
    page_number = int(request.rel_url.query.get('page', '0'))
    count = vehicle_collection.estimated_document_count()
    cursor = vehicle_collection.find(projection={'_id': False}).skip((page_number - 1) * PAGE_SIZE if page_number > 0 else 0).limit(PAGE_SIZE)
    page_data = list(cursor)
    page_data_string = json.dumps(page_data, indent=4)
    return web.Response(text=f"Number of documents: {count};\n Page {page_number};\n {page_data_string}")


async def start_background_tasks(app):
    """
    Set background to task to listen to a websocket
    """
    loop = asyncio.get_event_loop()
    app['ws_listener'] = loop.create_task(read_from_websocket(WEBSOCKET_URL))


async def cleanup_background_tasks(app):
    """
    Cancel previously scheduled task to listen to a websocket
    """
    app['ws_listener'].cancel()

if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.add_routes([web.get('/', send_data_from_db)])
    print(f"web app was started on {HOST}:{PORT}")
    web.run_app(app, host=HOST, port=PORT)



