import psycopg2

def verify_db_connection(connection, cur):
    try:
        cur.execute("SELECT;")
    except psycopg2.InterfaceError as e:
        print(e.message)
        return -1

    return 0

def add_to_database(connection, cur, user_id, keyword, unix_time):
    #checking if entry already exists
    sql = "SELECT * FROM Searches WHERE discord_id=%s AND keyword=%s;"
    val = (str(user_id), keyword)
    cur.execute(sql, val)
    entries = cur.fetchall()

    #if listing doesnt exist add to database
    if entries == []:
        val = (user_id, keyword, unix_time, 0)
        sql = """INSERT INTO Searches (discord_id, keyword, last_check, listings_found) VALUES (%s, %s, %s, %s)"""
        try:
            cur.execute(sql, val)
            connection.commit()
        except Exception as error:
            return False

        print("Entry inserted successfully into table")
        return True 
    else:
        return False 

def remove_from_database(connection, cur, user_id, keyword):
    sql = "SELECT * FROM Searches WHERE discord_id=%s AND keyword=%s;"
    val = (str(user_id), keyword, )
    try:
        cur.execute(sql, val)
        entries = cur.fetchall()
    except Exception as error:
        return False

    if entries == []:
        return False 
    else: 
        sql = "DELETE FROM Searches WHERE discord_id=%s AND keyword=%s;"
        val = (str(user_id), keyword, )
        cur.execute(sql, val)
        connection.commit()
        return True 

# updates the time for when a listing is found as well as incremements a variable containg number of listings found
def update_entry(connection, cur, user_id, keyword, new_time):
    sql = "UPDATE Searches SET last_check=%s, listings_found=listings_found+1 WHERE discord_id=%s AND keyword=%s"
    val = (str(new_time), str(user_id), keyword, )
    try:
        cur.execute(sql, val)
        connection.commit()
    except Exception as error:
        print(error)

def delete_all_user_entries(connection, cur, user_id):
    sql = "DELETE FROM Searches WHERE discord_id=%s;"
    val = (str(user_id), )
    try:
        cur.execute(sql, val)
        connection.commit()
    except Exception as error:
        print(error)
        return False
    return True

def get_user_entries(connection, cur, user_id):
    sql = "SELECT keyword, listings_found FROM Searches WHERE discord_id=%s;"
    val = (str(user_id), )
    try:
        cur.execute(sql, val)
        entries = cur.fetchall()
    except Exception as error:
        print(error)
        return None
    return entries

def get_all_entries(connection, cur):
    sql = "SELECT * FROM Searches;"
    try:
        cur.execute(sql)
        entries = cur.fetchall()
    except Exception as error:
        print(error)
        return None
    return entries

def add_new_user(connection, cur):
    sql = "UPDATE Stats SET all_users=all_users+1 WHERE name='main';"
    try:
        cur.execute(sql)
        connection.commit()
    except Exception as error:
        print(error)
        return False
    return True

def add_listing(connection, cur):
    sql = "UPDATE Stats SET all_listings=all_listings+1 WHERE name='main';"
    try:
        cur.execute(sql)
        connection.commit()
    except Exception as error:
        print(error)
        return False
    return True

def add_found_listings(connection, cur, num):
    sql = "UPDATE Stats SET all_found=all_found+%s WHERE name='main';"
    val = (num, )
    try:
        cur.execute(sql, val)
        connection.commit()
    except Exception as error:
        print(error)
        return False
    return True

def get_number_of_unique_users(connection, cur):
    sql = "SELECT COUNT(DISTINCT discord_id) FROM Searches;" 
    try:
        cur.execute(sql)
        count = cur.fetchall()
    except Exception as error:
        print(error)
        return None 
    return count 

def get_number_of_entries(connection, cur):
    sql = "SELECT COUNT(*) FROM Searches;" 
    try:
        cur.execute(sql)
        count = cur.fetchall()
    except Exception as error:
        print(error)
        return None 
    return count 

def connect_to_database(user, database, password, host, port):
    myConnection = psycopg2.connect(
            user=user,
            database=database,
            password=password,
            host=host,
            port=port)
    return myConnection
