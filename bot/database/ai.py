from ast import literal_eval

class aiDB:
    def __init__(self, dbConnection):
        self.db = dbConnection
    
    async def get(self):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT channels FROM ai")
        await conn.close()
        return x

    async def add(self, channel_id):
        conn = await self.db.get_connection()
        x = await self.get()
        channels = literal_eval(x[0])
        channels.append(channel_id)
        await conn.execute("DELETE FROM ai")
        await conn.execute("INSERT INTO ai(channels) VALUES ($1)", f"{str(channels)}")
        await conn.close()
    
    async def remove(self, channel_id):
        conn = await self.db.get_connection()
        x = await self.get()
        channels: list = literal_eval(x[0])
        channels.remove(channel_id)
        await conn.execute("DELETE FROM ai")
        await conn.execute("INSERT INTO ai(channels) VALUES ($1)", f"{str(channels)}")
        await conn.close()