import psycopg2
from psycopg2.extras import RealDictCursor

CONFIG_DB_NAME = "lora"
CONFIG_DB_USER = "postgres"
CONFIG_DB_PASSWORD = "Welc0me!"
CONFIG_DB_HOST = "127.0.0.1"
CONFIG_DB_PORT = "5432"


def getStockPriceFromDB(ticker, startdate, timeWindowsInDays):
    with psycopg2.connect(database=CONFIG_DB_NAME, user=CONFIG_DB_USER,
                          password=CONFIG_DB_PASSWORD, host=CONFIG_DB_HOST, port=CONFIG_DB_PORT) as conn:

        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            '''
            SELECT 
                    day, 
                    price 
            FROM    imported_closes 
            WHERE   ticker = %s 
                    and day between to_date(%s, 'YYYYMMDD') - %s +1 and to_date(%s, 'YYYYMMDD')
            ORDER BY day DESC
            ''',
            (ticker,
             startdate,
             timeWindowsInDays,
             startdate
             )
        )

        records = cur.fetchall()
        stockResultList = []
        for record in records:
            stockResult = {}
            stockResult['day'] = record['day']
            stockResult['price'] = record['price']
            stockResultList.append(stockResult)

        return stockResultList
