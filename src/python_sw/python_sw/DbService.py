import oracledb


class DbService:
    def __enter__(self):
        self.connection = oracledb.connect(
            dsn="127.0.0.1/dbuebung", user="dbuser", password="test"
        )
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


async def get_db_service():
    with DbService() as db:
        yield db
