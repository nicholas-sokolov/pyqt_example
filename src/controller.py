from src.signals import signals
from src.sql import Sql


class Controller:

    def __init__(self):
        self.sql = None
        self.connect_signals()

    def connect_signals(self):
        signals.make_query.connect(self.make_query)

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
