import oracledb


class DbService:
    def __init__(self, autocommit, commit_on_exit, commit_on_error):
        self._autocommit = autocommit
        self._commit_on_exit = commit_on_exit
        self._commit_on_error = commit_on_error


    def __enter__(self):
        self.connection = oracledb.connect(
            dsn="127.0.0.1/dbuebung", user="dbuser", password="test"
        )
        self.connection.autocommit = self._autocommit
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._autocommit:
            if self._commit_on_error or (exc_type is None and self._commit_on_exit):
                self.connection.commit()
        self.connection.close()

def get_db(autocommit = True, commit_on_exit = True, commit_on_error = False):
    async def get_db_service():
        with DbService(autocommit, commit_on_exit, commit_on_error) as db:
            yield db
    return get_db_service
