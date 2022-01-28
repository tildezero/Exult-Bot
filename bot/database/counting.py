from ast import literal_eval

class countingDB:
    def __init__(self, dbConnection):
        self.db = dbConnection
    
    async def get(self, channel_id: int):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT number, user_id, blacklist FROM counting WHERE channel_id = $1", channel_id)
        await conn.close()
        return x

    async def add(self, channel_id: int):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO counting(channel_id, number, user_id, blacklist) VALUES ($1, $2, $3, $4)", channel_id, 0, 0, "[]")
        await conn.close()

    async def blacklist(self, channel_id: int, user_id: int):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT channel_id, number, user_id, blacklist FROM counting WHERE channel_id = $1", channel_id)
        updated = literal_eval(x[3])
        updated.append(user_id)
        await conn.execute("UPDATE counting SET blacklist = $1 WHERE channel_id = $2", f"{updated}", channel_id)
        await conn.close()

    async def whitelist(self, channel_id: int, user_id: int):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT channel_id, number, user_id, blacklist FROM counting WHERE channel_id = $1", channel_id)
        updated: list = literal_eval(x[3])
        updated.remove(user_id)
        await conn.execute("UPDATE counting SET blacklist = $1 WHERE channel_id = $2", f"{updated}", channel_id)
        await conn.close()

    async def update(self, channel_id: int, number: int, user_id: int):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE counting SET number = $1 WHERE channel_id = $2", number, channel_id)
        await conn.execute("UPDATE counting SET user_id = $1 WHERE channel_id = $2", user_id, channel_id)
        await conn.close()

    async def reset(self, channel_id):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE counting SET number = 0 WHERE channel_id = $1", channel_id)
        await conn.execute("UPDATE counting SET user_id = 0 WHERE channel_id = $1", channel_id)
        await conn.close()
    
    async def remove(self, channel_id: int):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM counting WHERE channel_id = $1", channel_id)
        await conn.close()