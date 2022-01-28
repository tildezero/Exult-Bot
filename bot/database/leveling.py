class LevelingDB:
    def __init__(self, con):
        self.dbConnection = con
    
    async def add_xp(self, user, xp, guild):
        db = await self.dbConnection.get_connection()
        if await self.get_all(user, guild) == []:
            await self.insert(user, guild, xp, 1)
        else:
            await db.execute("UPDATE leveling SET xp=xp+$1 WHERE id=$2 AND guild=$3", xp, user, guild)
        res = await db.fetch("SELECT xp, level FROM leveling WHERE id=$1 AND guild=$2", user, guild)
        await db.close()

        return res
    
    async def get_xp(self, user, guild):
        db = await self.dbConnection.get_connection()
        res = await db.fetch("SELECT xp FROM leveling WHERE id=$1 AND guild=$2", user, guild)
        await db.close()
        return res
    
    async def get_level(self, user, guild):
        db = await self.dbConnection.get_connection()
        res = await db.fetch("SELECT level FROM leveling WHERE id=$1 AND guild=$2", user, guild)
        await db.close()
        return res
    
    async def levelup(self, user, guild, xp=0):
        db = await self.dbConnection.get_connection()
        await db.execute("UPDATE leveling SET level=level+1, xp=$1 WHERE id=$2 and guild=$3", xp, user, guild)
        await db.close()
    
    async def insert(self, user, guild, xp, lvl):
        db = await self.dbConnection.get_connection()
        await db.execute("INSERT INTO leveling(id, guild, xp, level) VALUES ($1, $2, $3, $4)", user, guild, xp, lvl)
        await db.close()
    
    async def get_all(self, user, guild):
        db = await self.dbConnection.get_connection()
        res = await db.fetch("SELECT * FROM leveling WHERE id=$1 AND guild=$2", user, guild)
        await db.close()
        return res
    
    async def remove(self, user, guild):
        db = await self.dbConnection.get_connection()
        await db.execute("DELETE FROM leveling WHERE id=$1 AND guild=$2", user, guild)
        await db.close()

    async def get_custom_message(self, guild):
        try:
            db = await self.dbConnection.get_connection()
            res = await db.fetch("SELECT custom_message FROM levelingc WHERE guild=$1", guild)
            await db.close()
            return res
        except Exception:
            return None
    
    async def get_custom_channel(self, guild):
        try:
            db = await self.dbConnection.get_connection()
            res = await db.fetch("SELECT custom_channel FROM levelingc WHERE guild=$1", guild)
            await db.close()
            return res
        except Exception:
            return None
    
    # NOTE: Should we have a funtion to get the custom channel and message? Or just use the get_all function?
    
    async def delete_all_data(self, guild):
        db = await self.dbConnection.get_connection()
        await db.execute("DELETE FROM leveling WHERE guild=$1", guild)
        await db.close()
    
    async def set_bio(self, user, msg):
        db = await self.dbConnection.get_connection()
        await db.execute("UPDATE leveling SET bio=$1 WHERE id=$2", msg, user)
        await db.close()
    
    async def get_bio(self, user):
        db = await self.dbConnection.get_connection()
        res = await db.fetch("SELECT bio FROM leveling WHERE id=$1", user)
        await db.close()
        return res