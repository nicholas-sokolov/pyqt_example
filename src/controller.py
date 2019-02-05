from src.signals import signals
from src.sql import Sql


class Controller:

    def __init__(self):
        self.sql_connect = None
        self.connect_signals()

    def connect_signals(self):
        signals.make_query.connect(self.make_query)
        signals.set_connection.connect(self.set_connect)

    def set_connect(self, database):
        if not database:
            signals.show_status.emit(f'No such database')
            return

        if self.sql_connect:
            self.sql_connect.close()
            signals.connection_button_trigger.emit()
            signals.show_status.emit(f'Close connect with {database}')
            self.sql_connect = None
            return

        try:
            sql = Sql(database)
            self.sql_connect = sql.connect
            signals.show_status.emit(f'Connect to {database}')
            signals.connection_button_trigger.emit()
        except Exception as err:
            signals.error_received.emit(f'{err}')

    def make_query(self, connection, query):
        """

        :param str connection:
        :param str query:
        :return:
        """
        self.sql = Sql(connection)
        try:
            if query.lower().startswith('select'):
                header, result = self.sql.select(query)
                signals.draw_table.emit(header, result)
            elif query.lower().startswith('create') or query.lower().startswith('insert'):
                self.sql.create_insert(query)
            else:
                signals.error_received('Unknown query')
        except Exception as err:
            signals.error_received.emit(f'{err}')
