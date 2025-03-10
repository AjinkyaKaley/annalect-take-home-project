from psycopg.rows import class_row
from models.oil_record import oil_record

def get_list(colname:str, filter:str, page_num:int, page_limit:int, conn):
    colname = colname.strip()
    filter = filter.strip()

    with conn.cursor(row_factory=class_row(oil_record)) as cur:
        query = f"""
                    SELECT * 
                    FROM 
                        commodity.oil o
                    WHERE o.{colname} = '{filter}'
                    LIMIT {page_limit}
                    OFFSET {page_num}
                """
        cur.execute(query)
        return cur.fetchall()

def get_record(id, conn):
    with conn.cursor(row_factory=class_row(oil_record)) as curr:
        query = f"""
                    SELECT *
                    FROM
                        commodity.oil o
                    WHERE o.id = {str(id)}
                """
        curr.execute(query)
        return curr.fetchall()

def insert_record(data, conn)->int:
    with conn.cursor() as cur:
        columns = ",".join(list(data.model_dump().keys()))
        values  = tuple(map(str,data.model_dump().values()))

        query = f"""
                    INSERT INTO commodity.oil ({columns})
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id
                """
        cur.execute(query, values)
        conn.commit()

        id = cur.fetchone()[0]
        return id
    
def check_valid_id(id: int, conn):
    query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM commodity.oil
                    WHERE id=%s
                )
            """
    with conn.cursor() as cur:
        params = [id]
        cur.execute(query, params)
        return cur.fetchone()[0]

def update_record(id, data, conn):
    data = data.model_dump()
    update_col_values = []
    values = []
    for k,v in data.items():
        if v is not None:
            update_col_values.append(f"{k}=%s")
            values.append(v)

    values.append(id)
    update_cols = ",".join(update_col_values)

    query = f"""
                UPDATE commodity.oil
                SET {update_cols}
                WHERE id = %s
            """

    with conn.cursor() as cur:
        cur.execute(query, values)
        conn.commit()

        return get_record(id, conn)
    
def delete_record(id:int, conn):
    query = """
            DELETE FROM commodity.oil
            WHERE id=%s; 
            """
    values = [id]

    with conn.cursor() as cur:
        cur.execute(query, values)
        conn.commit()