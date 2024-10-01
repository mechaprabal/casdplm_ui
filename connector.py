import mariadb

def db_query(
        db_username: str,
        db_pass: str,
        db_hostname: str,
        db_port: int,
        db_name: str,
        user_query: str,
):
    '''
    This function can connect and manage the connection with
    MariaDB server
    '''
    try:
        conn = mariadb.connect(
            user=db_username,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name,
        )

        print("connection succesful")

        # Execute the user query
        cur = conn.cursor()

        cur.execute(user_query)

        rows = cur.fetchall()

        for row in rows:
            print(row)
    
    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


    return

db_query(
    db_username="root",
    db_pass="root123",
    db_hostname="localhost",
    db_port=3306,
    db_name="cw_emissions",
    user_query="select count(*) from historical_data",
)