import psycopg2 as pg

def get_connection():
    return pg.connect(host='mydatabase.c2z535twmu4p.us-west-2.rds.amazonaws.com',
                 database='postgres',
                 user='postgres',
                 password='password',
                 port = '5432',
                 connect_timeout=3,
                )


def fetchQuery(query):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query)
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return rows, cols


def runQuery(query, response=False, commit=False):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query)
        rows, cols = None, None
        if response:
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
        if commit:
            con.commit()
        cur.close()
        return rows, cols
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return None, None
