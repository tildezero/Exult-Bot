# class EconomyDB:
#     def __init__(self, db):
#         self.dbConnection = dbConnection

#     def get_balance(self, user_id):
#         db = self.dbConnection.get_connection()
#         res = await db.fetch("SELECT wallet, bank, bank_limit FROM economy WHERE user_id=$1", user_id)
#         db.close()
#         return res

#     def update_balance(self, user_id, wallet, bank):
#         db = self.dbConnection.get_connection()
#         try:
#             await db.execute("UPDATE economy SET wallet=$1, bank=$2 WHERE user_id=$3", balance, wallet, user_id)
#             await db.close()
#         except Exception as e:
#             return "Could not update table ECONOMY"
    
#     def add_balance(self, user_id, wallet, bank):
#         db = self.dbConnection.get_connection()
#         try:
#             await db.execute("INSERT INTO economy(wallet, bank, user_id, items) VALUES($1, $2, $3, $4)", wallet, bank, user_id, "")
#             await db.close()
#         except Exception as e:
#             return "Could not update table ECONOMY"
    
#     def remove_balance(self, user_id):
#         db = self.dbConnection.get_connection()
#         try:
#             await db.execute("DELETE FROM economy WHERE user_id=$1", user_id)
#             await db.close()
#         except Exception as e:
#             return "Could not update table ECONOMY\nreason:{}".format(e)
        
#     def get_items(self, user_id):
#         db = self.dbConnection.get_connection()

#         try:
#             x = await db.fetch("SELECT items FROM economy WHERE user_id=$1", user_id)
#             await db.close()
#         except Exception as e:
#             return "Could not fetch from table ECONOMY\nreason:{}".format(e)
    
#     def update_items(self, user_id, items):
#         db = self.dbConnection.get_connection()
#         try:
#             await db.execute("UPDATE economy SET items=$1 WHERE user_id=$2", items, user_id)
#             await db.close()
#         except Exception as e:
#             return "Could not update table ECONOMY\nreason:{}".format(e)