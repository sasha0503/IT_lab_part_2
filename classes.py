from typing import List, Any

"""my own db manager"""


class Database:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"

        self.name = name
        self.tables: List[Table] = []


class Column:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"
        self.name = name
        self.type = None

    def validate(self, value):
        pass


class Table:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"

        self.name = name
        self.columns: List[Column] = []
        self.rows: List[Row] = []

    def search(self, filter_list: List[Any]):
        """
        :param filter_list: list of each column's value
        :return: rows that match the filter
        """
        assert len(filter_list) == len(self.columns), "filter_list must have the same length as columns"
        filtered_rows = [row for row in self.rows if all(
            filter_val is None or row_val == filter_val for row_val, filter_val in zip(row.values, filter_list))]

        return filtered_rows

    def add_column(self, column: Column):
        if not isinstance(column, Column):
            raise TypeError("column must be an instance of Column")

        for column_ in self.columns:
            if column_.name == column.name:
                raise ValueError("column with this name already exists")

        self.columns.append(column)


class Row:
    def __init__(self, table: Table, values: List[Any]):
        self.table = table
        self.values = values

    def __getitem__(self, item):
        return self.values[item]


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = int

    def validate(self, value):
        return isinstance(value, int)


class RealColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = float

    def validate(self, value):
        return isinstance(value, float)


class TextColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = str

    def validate(self, value):
        return isinstance(value, str)


class CharColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = str

    def validate(self, value):
        return isinstance(value, str) and len(value) == 1
