
from binance.websockets import BinanceSocketManager
import websocket, json, numpy, pandas
import config
from algo_functions import *
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)
bm = BinanceSocketManager(client)

print("success")