from flask import Flask, render_template, request
from classes import Database, Table, IntegerColumn, TextColumn, Row

app = Flask(__name__)

# Create a Database instance
db = Database("MyDatabase")

# Create a Table instance with columns
table = Table("MyTable")
table.add_column(IntegerColumn("ID"))
table.add_column(TextColumn("Name"))
db.tables.append(table)

# Create some sample rows
table.rows.append(Row(table, [1, "John"]))
table.rows.append(Row(table, [2, "Alice"]))


@app.route('/')
def index():
    return render_template('app.html', rows=table.rows, columns=table.columns)


@app.route('/search', methods=['POST'])
def search():
    filter_list = [request.form[column.name] for column in table.columns]
    filter_list = [i or None for i in filter_list]
    filtered_rows = table.search(filter_list)
    return render_template('app.html', rows=filtered_rows, columns=table.columns)


if __name__ == '__main__':
    app.run(debug=True)
