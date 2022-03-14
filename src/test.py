import connect_database

if __name__ == "__main__":
    dic = {'sha256': '123'}
    db = connect_database.open_database('crawl')
    connect_database.save(db=db, table_name='remove_duplication', val=dic, unique_keys=('sha256',))
    connect_database.close_database(db=db)
