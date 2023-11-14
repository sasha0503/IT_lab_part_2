from flask import Flask, render_template, request, jsonify

from classes import Table, Column, Row
from custom_logger import logger
from utils import load_db_from_request, save_db_to_file

app = Flask(__name__)

logger.debug("############# starting app")


@app.route('/')
def index():
    db = load_db_from_request(request)
    logger.debug(f"GET index from db '{db.name}'")
    logger.debug(f"tables: {db.list_tables()}")
    return render_template('index.html', db_name=db.name, tables=db.list_tables())


@app.route('/get_table/<table_name>', methods=['GET'])
def get_table(table_name):
    db = load_db_from_request(request)
    logger.debug(f"GET get_table from db '{db.name}'")
    table = db.get_table(table_name)
    return render_template('table_search.html', table_name=table.name, rows=table.rows, columns=table.columns)


@app.route('/del_table/<table_name>', methods=['DELETE'])
def del_table(table_name):
    db = load_db_from_request(request)
    logger.debug(f"DELETE del_table/{table_name} from db '{db.name}'")
    db.del_table(table_name)
    save_db_to_file(db)
    return jsonify({"success": True})


@app.route('/edit_table/<table_name>', methods=['GET'])
def edit_table(table_name):
    db = load_db_from_request(request)
    logger.debug(f"POST edit_table/{table_name} to db '{db.name}'")
    table = db.get_table(table_name)
    return render_template('edit_table.html', table_name=table.name, columns=table.columns)


@app.route('/edit_rows/<table_name>', methods=['GET'])
def edit_rows(table_name):
    db = load_db_from_request(request)
    logger.debug(f"POST edit_table/{table_name} to db '{db.name}'")
    table = db.get_table(table_name)
    existing_rows = [row.values for row in table.rows]
    columns = [{"name": col.name} for col in table.columns]
    return render_template('edit_rows.html', table_name=table.name, existingRows=existing_rows, columns=columns)


@app.route('/save_edit/<table_name>', methods=['POST'])
def save_edit(table_name):
    db = load_db_from_request(request)
    logger.debug(f"POST save_edit/{table_name} to db '{db.name}'")
    table = db.get_table(table_name)
    new_cols = {col["name"]: col["type"] for col in request.json['columns']}
    old_cols = {col.name: col.type for col in table.columns}
    for col_name, col_type in new_cols.items():
        if col_name not in old_cols:
            type_col = Column.create_type_column(col_type, col_name)
            table.add_column(type_col)
        elif old_cols[col_name] != col_type:
            table.del_column(col_name)
            type_col = Column.create_type_column(col_type, col_name)
            table.add_column(type_col)
    for col_name, col_type in old_cols.items():
        if col_name not in new_cols:
            table.del_column(col_name)
    save_db_to_file(db)
    return jsonify({"success": True})


@app.route('/save_rows', methods=['POST'])
def save_rows():
    data = request.json
    table_name = data['table_name']
    rows = data['rows']
    db = load_db_from_request(request)
    logger.debug(f"POST save_rows/{table_name} to db '{db.name}'")

    table = db.get_table(table_name)
    table.rows = []
    for row_ in rows:
        for i, val in enumerate(row_):
            if val == "":
                row_[i] = None
        row = Row(table, row_)
        table.add_row(row)
    save_db_to_file(db)
    return jsonify({"success": True})


@app.route('/add_table/<table_name>', methods=['POST'])
def add_table(table_name):
    db = load_db_from_request(request)
    logger.debug(f"POST add_table/{table_name} to db '{db.name}'")
    table = Table(table_name)
    db.add_table(table)
    save_db_to_file(db)
    return jsonify({"success": True})


@app.route('/json_table/<table_name>', methods=['GET'])
def json_table(table_name):
    db = load_db_from_request(request)
    logger.debug(f"GET get_table/{table_name} from db '{db.name}'")
    table_res = db.get_table(table_name)
    return jsonify(table_res.to_json())


@app.route('/search/<table_name>', methods=['GET', 'POST'])
def search(table_name):
    db = load_db_from_request(request)
    logger.debug(f"POST search in db '{db.name}'")
    table = db.get_table(table_name)
    filter_list = [request.form[column.name] for column in table.columns]
    filter_list = [i or None for i in filter_list]
    logger.debug(f"filter_list: {filter_list}")
    filtered_rows = table.search(filter_list)
    logger.debug(f"filtered_rows: {filtered_rows}")
    return render_template('table_search.html', table_name=table_name, rows=filtered_rows, columns=table.columns)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)
