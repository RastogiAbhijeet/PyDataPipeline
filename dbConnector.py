import pyodbc

SQL_DATABASES = {
    "MSSQL": "MSSQL"
}

class DatabaseConnection(object):
    def __init__(self, connectionString, db):
        self.dbType = db
        self.dbConn = pyodbc.connect(connectionString)

    def getData(self, query, **params):
        data = []

        try:
            cursor = self.dbConn.cursor()

            cursor.execute(query)
            for row in cursor.execute(query):
                data.append(row)

            return data

        except Exception as err:
            print(err)
