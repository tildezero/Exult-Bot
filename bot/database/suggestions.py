from datetime import datetime, timedelta
from ast import literal_eval

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
        await conn.execute("DELETE FROM suggestions WHERE guild_id = $1", guild_id)
        await conn.close()

    async def getconf(self, guild_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT channel_id, safemode FROM suggestconf WHERE guild_id = $1", guild_id)
        await conn.close()
        return x

    async def add(self, guild_id, user_id, suggestion):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO suggestions(guild_id, user_id, suggestion, created_at) VALUES ($1, $2, $3, $4)", guild_id, user_id, suggestion, str(datetime.utcnow()))
        await conn.close()

    async def confirm(self, suggestion_id, message_id):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE suggestions SET message_id = $1 WHERE suggestion_id = $2", message_id, suggestion_id)
        await conn.execute("UPDATE suggestions SET upvotes = $1 WHERE suggestion_id=$2", "[]", suggestion_id)
        await conn.execute("UPDATE suggestions SET downvotes = $1 WHERE suggestion_id=$2", "[]", suggestion_id)
        await conn.close()

    async def getsuggestion(self, suggestion_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT * FROM suggestions WHERE suggestion_id = $1", suggestion_id)
        await conn.close()
        return x

    async def get_id(self, guild_id, user_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT suggestion_id FROM suggestions WHERE guild_id = $1 and user_id = $2", guild_id, user_id)
        await conn.close()
        return x

    async def remove(self, suggestion_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM suggestions WHERE suggestion_id = $1", suggestion_id)
        await conn.close()

    async def getvotes(self, suggestion_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT upvotes, downvotes FROM suggestions WHERE suggestion_id = $1", suggestion_id)
        await conn.close()
        return x

    async def updatevote(self, suggestion_id, upvote=None, downvote=None):
        totalvotes = await self.getvotes(suggestion_id)
        upvotes = totalvotes[0][0]
        upvotes = literal_eval(upvotes)
        downvotes = totalvotes[0][1]
        downvotes = literal_eval(downvotes)
        if upvote:
            if upvote in upvotes:
                upvotes.remove(upvote)
            elif upvote not in upvotes:
                upvotes.append(upvote)
            if upvote in downvotes:
                downvotes.remove(upvote)
        elif downvote:
            if downvote in downvotes:
                downvotes.remove(downvote)
            elif downvote not in downvotes:
                downvotes.append(downvote)
            if downvote in upvotes:
                upvotes.remove(downvote)
        conn = await self.db.get_connection()
        await conn.execute("UPDATE suggestions SET upvotes = $1 WHERE suggestion_id = $2", f"{upvotes}", suggestion_id)
        await conn.execute("UPDATE suggestions SET downvotes = $1 WHERE suggestion_id = $2", f"{downvotes}", suggestion_id)
        await conn.close()

    async def updatechannel(self, guild_id, channel_id):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE suggestconf SET channel_id = $1 WHERE guild_id = $2", channel_id, guild_id)
        await conn.close()

    async def updatesafemode(self, guild_id, safemode):
        conn = await self.db.get_connection()
        if not safemode:
            await conn.execute("UPDATE suggestconf SET safemode = NULL WHERE guild_id = $1", guild_id)
        if safemode:
            await conn.execute("UPDATE suggestconf SET safemode = $1 WHERE guild_id = $2", safemode, guild_id)
        await conn.close()
