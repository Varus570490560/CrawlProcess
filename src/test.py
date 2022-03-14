import connect_database

if __name__ == "__main__":
    db = connect_database.open_database(database_name='test')
    dic1 = {'a': 1, 'b': 3, 'c': 4}
    dic2 = {'a': 2, 'b': 3, 'c': 3}
    res = connect_database.save(db=db, table_name='table_name', val=dic2, unique_keys=('a', 'b'))
    print(res)
    connect_database.close_database(db=db)