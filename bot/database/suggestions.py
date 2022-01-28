from datetime import datetime, timedelta

class SuggestDB:
    def __init__(self, dbConnection):
        self.db = dbConnection
    
    async def setup(self, guild_id, channel_id, safemode):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO suggestconf(guild_id, channel_id, safemode) VALUES ($1, $2, $3)", guild_id, channel_id, safemode)
        await conn.close()

    async def setupnon(self, guild_id, channel_id):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO suggestconf(guild_id, channel_id) VALUES ($1, $2)", guild_id, channel_id)
        await conn.close()

    async def shutdown(self, guild_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM suggestconf WHERE guild_id = $1", guild_id)
        await conn.close()

    async def getconf(self, guild_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT channel_id, safemode FROM suggestconf WHERE guild_id = $1", guild_id)
        await conn.close()
        return x

    async def add(self, guild_id, user_id, suggestion):
        conn = await self.db.get_connection()
        x = await conn.execute("INSERT INTO suggestions(guild_id, user_id, suggestion, created_at) VALUES ($1, $2, $3, $4)", guild_id, user_id, suggestion, str(datetime.utcnow()))
        await conn.close()
        return x

    async def confirm(self, suggestion_id, message_id):
        conn = await self.db.get_connection()
        await conn.execite("UPDATE suggestions SET message_id = $1 WHERE suggestion_id = $2", message_id, suggestion_id)
        await conn.close()

    async def getsuggestion(self, suggestion_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT * FROM suggestions WHERE suggestion_id = $1", suggestion_id)
        await conn.close()
        return x

    async def get_id(self, guild_id, user_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT suggestion_id FROM suggestions WHERE guild_id = $1 and user_id = $2", guild_id, user_id)
        return x
