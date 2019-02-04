from src.signals import signals
from src.sql import Sql


class Controller:

    def __init__(self):
        self.connect_signals()

    def connect_signals(self):
        signals.make_query.connect(self.make_query)

    @staticmethod
    def make_query(connection, query):
        """

        :param str connection:
        :param str query:
        :return:
        """
        sql = Sql(connection)
        try:
            if query.lower().startswith('select'):
                header, result = sql.select(query)
                signals.draw_table.emit(header, result)
            elif query.lower().startswith('create'):
                sql.create(query)
            elif query.lower().startswith('insert'):
                sql.insert(query)

        except Exception as err:
            signals.error_received.emit(f'{err}')
