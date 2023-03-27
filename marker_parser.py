import json

from rustplus import RustSocket

with open("config.json", "r") as input_file:
    player_data = json.load(input_file)


class GettingInfo:
    def __init__(self, IP, PORT, STEAMID, PLAYERTOKEN):
        self.IP = IP
        self.PORT = PORT
        self.STEAMID = STEAMID
        self.PLAYERTOKEN = PLAYERTOKEN
        self.rust_socket = RustSocket(self.IP, self.PORT, self.STEAMID, self.PLAYERTOKEN)

    async def get_map(self):
        await self.rust_socket.connect()
        map_data = await self.rust_socket.get_raw_map_data()
        await self.rust_socket.disconnect()
        return map_data

    async def get_markers(self):
        await self.rust_socket.connect()
        markers_data = await self.rust_socket.get_markers()
        await self.rust_socket.disconnect()
        return markers_data


get_info = GettingInfo(player_data["IP"], player_data["PORT"], player_data["STEAMID"], player_data["PLAYERTOKEN"])