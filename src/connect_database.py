import hashlib
import hmac

import pymysql
import import_config


def open_database(database_name: str):
    crawl_config = import_config.CrawlConfig()
    try:
        db = pymysql.connect(host=crawl_config.mysql_host, user=crawl_config.mysql_user,
                             password=crawl_config.mysql_password, port=int(crawl_config.mysql_port),
                             database=database_name,
                             autocommit=True)
    except pymysql.Error as e:
        print(e)
        return None
    return db


def close_database(db: pymysql.connections.Connection):
    db.close()


def execute_sql(db: pymysql.connections.Connection, sql: str, args: tuple = None):
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        return cursor.fetchall()
    except pymysql.Error as e:
        print(e)
        return None
    finally:
        cursor.close()


def save(db: pymysql.connections.Connection, table_name: str, val: dict, unique_keys: tuple = None):
    crawl_db: pymysql.Connect.db = None
    sha256: str = ''
    if unique_keys is not None:
        lst: list = list()
        for unique_key in unique_keys:
            lst.append(val[unique_key])
        sha256: str = generate_sha256(unique_values=tuple(lst))
        sha256_dict = {'sha256': sha256}
        crawl_db = open_database('crawl')
        if save(db=crawl_db, table_name='remove_duplication', val=sha256_dict) is False:
            reason = {}
            for unique_key in unique_keys:
                reason[unique_key] = val[unique_key]
            print("Duplicate insert at: ", str(reason))
            return False
        close_database(crawl_db)
    sql: str = "INSERT INTO `" + table_name + "` (" + keys_to_string(val=val) + ")VALUES(" + values_to_string(
        val=val) + ");"
    if execute_sql(db=db, sql=sql) is None:
        if crawl_db is not None:
            execute_sql(db=crawl_db, sql="DELETE FROM `remove_duplication` WHERE `sha256` = %s;", args=(sha256,))
        return False
    else:
        return True


def keys_to_string(val: dict):
    res: str = ''
    for key in val.keys():
        key = '`' + key + '`'
        res = res + key
        res = res + ','
    res = res[:-1]
    return res


def values_to_string(val: dict):
    res: str = ''
    for value in val.values():
        value_str = str(value)
        value_str = value_str.replace("'", "\\'")
        value_str = value_str.replace('"', '\\"')
        value_str = "'" + value_str + "'"
        res = res + value_str

        res = res + ','
    res = res[:-1]
    return res


def generate_sha256(unique_values: tuple):
    string: str = ''
    for unique_value in unique_values:
        string = string + str(unique_value)
    return hmac.new(string.encode('utf-8'), digestmod=hashlib.md5).hexdigest().upper()
