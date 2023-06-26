from table_management import table_dict
import MySQLdb


def import_from_db(server, user, password, database) :
    db = MySQLdb.connect(server, user, password, database)
    cursor = db.cursor()
    print('Connected to {0}!'.format(database))

    cursor.execute(
        "select TABLE_NAME from INFORMATION_SCHEMA.TABLES "
        + "where TABLE_SCHEMA = '{0}' and TABLE_TYPE = 'BASE TABLE'".format(database)
    )
    data = cursor.fetchall()
    table_names = []
    for row in data :
        table_names.append(row[0])
    db_table_dict = {}
    for table_name in table_names :
        cursor.execute(
            "select DATA_TYPE, COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS "
            + "where TABLE_SCHEMA = '{0}' and TABLE_NAME = '{1}'".format(database, table_name)
            + "order by ORDINAL_POSITION"
        )
        data = cursor.fetchall()
        table_types = []
        table_keys = []
        for row in data :
            table_types.append(row[0])
            table_keys.append(row[1])
        db_table_dict[table_name] = [table_types, table_keys]
    for table_name in db_table_dict :
        cursor.execute("select * from {0}".format(table_name))
        data = cursor.fetchone()
        while data :
            db_table_dict[table_name].append(list(data))
            data = cursor.fetchone()
        print('Imported table {0}...'.format(table_name))
    table_dict.update(db_table_dict)
    print('Imported all tables!')

    db.close()
    print('Disconnected from {0}.'.format(database))
