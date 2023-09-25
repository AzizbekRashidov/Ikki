import sqlite3
class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER UNIQUE,
            user_id INTEGER NOT NULL UNIQUE,
            Name varchar(255) NOT NULL,
            PRIMARY KEY (id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)

    def create_table_groups(self):
        sql = """
        CREATE TABLE Groups (
            id INTEGER UNIQUE,
            user_id INTEGER NOT NULL UNIQUE,
            PRIMARY KEY (id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def stat(self):
        return self.execute(f"SELECT COUNT(*) FROM Users;", fetchone=True)
    def stat_group(self):
        return self.execute(f"SELECT COUNT(*) FROM Groups;", fetchone=True)
    def add_group(self, user_id: int):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Groups(user_id) VALUES(?)
        """
        self.execute(sql, parameters=(user_id, ), commit=True)
    def add_user(self, user_id: int, name: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(user_id, Name) VALUES(?, ?)
        """
        self.execute(sql, parameters=(user_id, name), commit=True)

    def select_all_users(self):
        sql = """
         SELECT * FROM Users
         """
        return self.execute(sql, fetchall=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")