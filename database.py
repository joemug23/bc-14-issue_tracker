import sqlite3


class Database:
    # a class db to interact with the db

    # db settings
    db = sqlite3.connect('trial.db')
    db.row_factory = sqlite3.Row

    def create_table(self, sql):
        try:
            Database.db.execute(sql)
            Database.db.commit()
        except Exception as e:
            return "An error occurred: {}".format(e)

    @staticmethod
    def insert(table, params):
        # construct and call an insert data query
        try:
            slist = sorted(params.keys())
            values = [params[v] for v in slist]
            query = 'insert into {} ({}) values ({})'.format(table,
                                                             ', '.join(slist),
                                                             ', '.join('?' for i in range(len(values))))
            Database.db.execute(query, values)
            Database.db.commit()
            return "Data inserted successfully!"

        except Exception as e:
            return "an Error occurred: {}".format(e)

    @staticmethod
    def update(table, params):
        # construct and call an update query
        try:
            slist = sorted(params.keys())
            db_id = params[table + "_id"]
            query = 'update {} set {} where {} = {}'.format(table,
                                                            ','.join([v + "='{}'".format(params[v]) for v in slist]),
                                                            table + "_id", db_id)
            Database.db.execute(query)
            Database.db.commit()
            return "Data updated successfully!"
        except:
            return "An error occurred"

    @staticmethod
    def deleting(table, params):
        # Construct and call a delete query
        try:
            db_id = params[table + "_id"]
            query = 'delete from {} where {} = {}'.format(table, table + "_id", db_id)

            print(query)
            Database.db.execute(query)
            Database.db.commit()
            return "Data deleted Successfully"
        except Exception as e:
            return "An error occurred: {}".format(e)

    @staticmethod
    def select_all(table):
        try:
            results = {}
            query = 'select * from {}'.format(table)
            cursor = Database.db.execute(query)
            for row in cursor:
                # adding each row to the results dictionary
                results[row[table + "_id"]] = dict(row)
            print(results)
            return results
        except Exception as e:
            return "An error occurred: {}".format(e)

    @staticmethod
    def select_cond(table, conds):
        # Construct and call the query to select data with condition
        # conds is a string containing the condition to pass in the sql query
        try:
            results = {}
            query = 'select * from {} where {}'.format(table, conds)
            cursor = Database.db.execute(query)
            for row in cursor:
                # adding each row to the results dictionary
                results[row[table + "_id"]] = dict(row)
            return results

        except Exception as e:
            return "An error occurred: {}".format(e)


def main():
    # Database.select_all
    # db.row_factory = sqlite3.Row
    Database.db.execute("drop table if exists issues")
    Database.db.execute(
        'create table issues(issues_id INTEGER PRIMARY KEY, '
        'description text, '
        'department text, '
        'priority text, '
        'status text DEFAULT "open",'
        'comment text, '
        'assigned_to text Default "No one",'
        'raise_person text)')

    Database.db.execute("drop table if exists users")
    Database.db.execute(
        'create table users(users_id INTEGER PRIMARY KEY, '
        'username text, '
        'email text, '
        'status text DEFAULT "staff", '
        'department text, '
        'password text)')
    Database.insert('users', {'username':'Jonathan', 'email':'joemzih23@gmail.com', 'status': 'admin', 'department': 'Operation', 'password':'mugula'})
    Database.insert('users', {'username': 'joemug', 'email': 'joemzih23@gmail.com', 'status': 'staff',
                              'department': 'Operation', 'password': 'mugula'})

    # Database.insert('users', {'username': 'Mugula', 'password': 'pass'})
    # Database.insert('users', {'username': 'Zihalirwa', 'password': '456'})
    # Database.select_all('users')
    # db.execute('insert into users (username, password) values(?, ?)', ('Joemug', '123'))
    # db.execute('insert into users (username, password) values(?, ?)', ('joe', 'joe'))
    # Database.db.commit()
    # cursor = Database.db.execute('select * from users')
    # for row in cursor:
    #     print(dict(row))


if __name__ == '__main__': main()
