import uuid
from typing import List, Any

"""my own db manager"""


class Column:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"
        self.name = name
        self.type = None

    @staticmethod
    def create_type_column(type: str, name: str):
        assert isinstance(type, str), "type must be a string"
        assert isinstance(name, str), "name must be a string"

        if type == "int":
            return IntegerColumn(name)
        elif type == "float" or type == "double":
            return RealColumn(name)
        elif type == "str" or type == "text" or type == "string":
            return TextColumn(name)
        elif type == "char":
            return CharColumn(name)
        else:
            raise ValueError(f"unknown type {type}")

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
            filter_val is None or str(row_val) == str(filter_val) for row_val, filter_val in
            zip(row.values, filter_list))]

        return filtered_rows

    def add_column(self, column: Column):
        if not isinstance(column, Column):
            raise TypeError("column must be an instance of Column")

        for column_ in self.columns:
            if column_.name == column.name:
                raise ValueError("column with this name already exists")

        self.columns.append(column)

        for row in self.rows:
            row.values.append(None)

    def del_column(self, column_name: str):
        for i, column in enumerate(self.columns):
            if column.name == column_name:
                self.columns.remove(column)
                for row in self.rows:
                    row.values.pop(i)
                return
        raise ValueError(f"column {column_name} not found")

    def add_row(self, row):
        if not isinstance(row, Row):
            raise TypeError("row must be an instance of Row")

        for col, val in zip(self.columns, row.values):
            if not col.validate(val):
                raise ValueError(f"column {col.name} does not accept value {val}")

        for row_ in self.rows:
            if row_.id == row.id:
                raise ValueError("row with this id already exists")

        self.rows.append(row)

    def to_json(self):
        return {
            "name": self.name,
            "columns": [{"name": col.name, "type": col.type} for col in self.columns],
            "rows": [[str(val) for val in row.values] for row in self.rows]
        }


class Row:
    def __init__(self, table: Table, values: List[Any]):
        self.table = table
        self.values = values
        self.id = uuid.uuid4().hex

    def __getitem__(self, item):
        return self.values[item]


class Database:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"

        self.name = name
        self.tables: List[Table] = []

    def get_table(self, table_name: str):
        for table in self.tables:
            if table.name == table_name:
                return table
        raise ValueError(f"table {table_name} not found")

    def add_table(self, table: Table):
        if not isinstance(table, Table):
            raise TypeError("table must be an instance of Table")

        for table_ in self.tables:
            if table_.name == table.name:
                raise ValueError("table with this name already exists")

        self.tables.append(table)

    def list_tables(self):
        return [table.name for table in self.tables]

    def del_table(self, table_name: str):
        for table in self.tables:
            if table.name == table_name:
                self.tables.remove(table)
                return
        raise ValueError(f"table {table_name} not found")

    def to_json(self):
        return {
            "name": self.name,
            "tables": [table.to_json() for table in self.tables]
        }


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "int"

    def validate(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                return False
        return isinstance(value, int)


class RealColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "float"

    def validate(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return False
        return isinstance(value, float)


class TextColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "str"

    def validate(self, value):
        if value is None:
            return True
        return isinstance(value, str)


class CharColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "char"

    def validate(self, value):
        if value is None:
            return True
        return isinstance(value, str) and len(value) == 1
