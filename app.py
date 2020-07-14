from flask import Flask, g, jsonify, make_response
from flask_restplus import Api, Resource, fields
import sqlite3
from os import path

app = Flask(__name__)
api = Api(app, version='1.0', title='APIs for Code.Sydney Merchandises',
          description='This is a Flask-Restplus data service that allows a client to consume APIs related to Code.Sydney merchandises.',
          )

#Database helper
ROOT = path.dirname(path.realpath(__file__))
def connect_db():
    sql = sqlite3.connect(path.join(ROOT, "stocks.db"))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@api.route('/all')
class AllMerch(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieving all records from the database for all suburbs.')
    def get(self):
        db = get_db()
        details_cur = db.execute('select id, stockname, imagename from stocks')
        details = details_cur.fetchall()

        return_values = []

        for detail in details:
            detail_dict = {}
            detail_dict['id'] = detail['id']
            detail_dict['stockname'] = detail['stockname']
            detail_dict['imagename'] = detail['imagename']

            return_values.append(detail_dict)

        return make_response(jsonify(return_values), 200)

if __name__ == '__main__':
    app.run()