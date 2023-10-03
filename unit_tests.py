import unittest
from classes import Database, Table, Column, IntegerColumn, RealColumn, TextColumn, CharColumn, Row


class DatabaseTest(unittest.TestCase):
    def test_create_db_success(self):
        db = Database("test_db")
        self.assertEqual(db.tables, [])
        self.assertEqual(db.name, "test_db")

    def test_create_db_fail(self):
        with self.assertRaises(Exception):
            Database(1)

        with self.assertRaises(Exception):
            Database()


class TableTest(unittest.TestCase):
    def test_create_table_success(self):
        table = Table("test_table")
        self.assertEqual(table.rows, [])
        self.assertEqual(table.name, "test_table")
        self.assertEqual(table.columns, [])

    def test_create_table_fail(self):
        with self.assertRaises(Exception):
            Table(1)

        with self.assertRaises(Exception):
            Table()

    def test_search_success(self):
        table = Table("test_table")
        table.add_column(IntegerColumn("id"))
        table.add_column(TextColumn("name"))

        row1 = Row(table, [1, "John"])
        row2 = Row(table, [2, "Jane"])
        row3 = Row(table, [3, "John"])

        table.rows.append(row1)
        table.rows.append(row2)
        table.rows.append(row3)

        res = table.search([1, "John"])
        self.assertEqual(res, [row1])

        res = table.search([None, "John"])
        self.assertEqual(res, [row1, row3])

        res = table.search([None, None])
        self.assertEqual(res, [row1, row2, row3])

        res = table.search([1, 2])
        self.assertEqual(res, [])

    def test_search_fail(self):
        table = Table("test_table")
        table.add_column(IntegerColumn("id"))
        table.add_column(TextColumn("name"))

        row1 = Row(table, [1, "John"])
        row2 = Row(table, [2, "Jane"])
        row3 = Row(table, [3, "John"])

        table.rows.append(row1)
        table.rows.append(row2)
        table.rows.append(row3)

        with self.assertRaises(Exception):
            table.search(1)

        with self.assertRaises(Exception):
            table.search([1, 2, 3])

        with self.assertRaises(Exception):
            table.search([1, "John", 3])

    def test_add_column_success(self):
        table = Table("test_table")
        table.add_column(IntegerColumn("id"))
        table.add_column(TextColumn("name"))

        self.assertEqual(len(table.columns), 2)
        self.assertEqual(table.columns[0].name, "id")
        self.assertEqual(table.columns[1].name, "name")

    def test_add_column_fail(self):
        table = Table("test_table")

        with self.assertRaises(Exception):
            table.add_column(IntegerColumn("id"))
            table.add_column(TextColumn("id"))

        with self.assertRaises(Exception):
            table.add_column(1)


class ColumnTest(unittest.TestCase):
    def test_create_column_success(self):
        column = Column("test_column")
        self.assertEqual(column.name, "test_column")
        self.assertEqual(column.type, None)

    def test_create_column_fail(self):
        with self.assertRaises(Exception):
            Column(1)

        with self.assertRaises(Exception):
            Column()


class IntegerColumnTest(unittest.TestCase):
    def test_create_column_success(self):
        column = IntegerColumn("test_column")
        self.assertEqual(column.name, "test_column")
        self.assertEqual(column.type, int)

    def test_create_column_fail(self):
        with self.assertRaises(Exception):
            IntegerColumn(1)

        with self.assertRaises(Exception):
            IntegerColumn()

    def test_validate_success(self):
        column = IntegerColumn("test_column")
        self.assertTrue(column.validate(1))
        self.assertTrue(column.validate(0))
        self.assertTrue(column.validate(-1))

    def test_validate_fail(self):
        column = IntegerColumn("test_column")
        self.assertFalse(column.validate(1.0))
        self.assertFalse(column.validate(0.0))
        self.assertFalse(column.validate(-1.0))
        self.assertFalse(column.validate("1"))
        self.assertFalse(column.validate("0"))
        self.assertFalse(column.validate("-1"))


if __name__ == '__main__':
    unittest.main()
