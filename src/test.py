import connect_database

if __name__ == "__main__":
    db = connect_database.open_database(database_name='test')
    dic1 = {'a': 'xcsd"c'}
    res = connect_database.save(db=db, table_name='table2', val=dic1, unique_keys=('a',))
    print(res)
    connect_database.close_database(db=db)