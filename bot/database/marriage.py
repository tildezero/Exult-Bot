from ast import literal_eval

class marriageDB:
    def __init__(self, dbConnection):
        self.db = dbConnection
    
    async def get(self, user_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT marriages FROM marriages WHERE user_id = $1", user_id)
        await conn.close()
        return x

    async def check_existing(self, user_id, partner):
        conn = await self.db.get_connection()
        x = await self.get(user_id)
        if x:
            marriages = literal_eval(x[0])
            if int(partner) in marriages:
                return "You are already married to this user!"

    async def add(self, user_id, partner):
        conn = await self.db.get_connection()
        x = await self.get(user_id)
        if x:
            marriages = literal_eval(x[0])
            marriages.append(partner)
        else:
            marriages = [partner]
        await conn.execute("DELETE FROM marriages WHERE user_id = $1", user_id)
        await conn.execute("INSERT INTO marriages(user_id, marriages) VALUES ($1, $2)", user_id, f"{marriages}")
        await conn.close()
    
    async def remove(self, user_id, partner):
        conn = await self.db.get_connection()
        x = await self.get(user_id)
        marriages: list = literal_eval(x[0])
        marriages.remove(partner)
        await conn.execute("DELETE FROM marriages WHERE user_id = $1", user_id)
        await conn.execute("INSERT INTO marriages(user_id, marriages) VALUES ($1, $2)", user_id, f"{str(marriages)}")
        await conn.close()

    async def removeall(self, user_id):
        conn = await self.db.get_connection()
        x = await self.get(user_id)
        if len(x) > 0:
            await conn.execute("DELETE FROM marriages WHERE user_id = $1", user_id)
        elif len(x) == 0 or x is None:
            return "You are not married to anyone 💔"
        await conn.close()