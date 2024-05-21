import aiomysql


class Request:

    def __init__(self, connector: aiomysql.pool.Pool):
        self.connector = connector

    async def get_goods_db(self) -> tuple:
        query = '''
            SELECT SQL_NO_CACHE name, image_url FROM product_product;
        '''
        cur = await self.connector.cursor()
        await cur.execute(query)
        goods = await cur.fetchall()
        self.connector.close()
        return goods
