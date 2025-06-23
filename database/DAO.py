from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStore():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select * 
                    from stores"""
        cursor.execute(query)
        for row in cursor:
            result.append(Store(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllOrders(num):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select * 
                    from orders
                    where store_id = %s"""
        cursor.execute(query, (num, ))
        for row in cursor:
            result.append(Order(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeight(store):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select o.order_id as id, sum(o.quantity) as weightOrder
                    from order_items o, orders ord
                    where o.order_id = ord.order_id 
                    and ord.store_id = %s
                    group by o.order_id"""
        cursor.execute(query, (store,))
        for row in cursor:
            result.append((row["id"], int(row["weightOrder"]) ))
        cursor.close()
        conn.close()
        return result