from flask import Flask, g, jsonify, make_response
from flask_restplus import Api, Resource, fields
import sqlite3
from os import path

app = Flask(__name__)
api = Api(app, version='1.0', title='Data Service for NSW birth rate information by suburb',
          description='This is a Flask-Restplus data service that allows a client to consume APIs related to NSW birth rate information by suburb.',
          )

#Database helper
ROOT = path.dirname(path.realpath(__file__))
def connect_db():
    sql = sqlite3.connect(path.join(ROOT, "NSW_BIRTH_RATE.sqlite"))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@api.route('/all')
class TopBabyAll(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieving all records from the database for all suburbs.')
    def get(self):
        db = get_db()
        details_cur = db.execute('select YEAR, LOCALITY, SUBURB, STATE, POSTCODE, COUNT from NSW_BIRTH_RATE')
        details = details_cur.fetchall()

        return_values = []

        for detail in details:
            detail_dict = {}
            detail_dict['YEAR'] = detail['YEAR']
            detail_dict['LOCALITY'] = detail['LOCALITY']
            detail_dict['SUBURB'] = detail['SUBURB']
            detail_dict['STATE'] = detail['STATE']
            detail_dict['POSTCODE'] = detail['POSTCODE']
            detail_dict['COUNT'] = detail['COUNT']

            return_values.append(detail_dict)

        return make_response(jsonify(return_values), 200)


@api.route('/all/<string:SUBURB>', methods=['GET'])
class TopBabySuburb(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieving all records from the database for one suburb.')
    def get(self, SUBURB):
        db = get_db()
        details_cur = db.execute(
            'select YEAR, LOCALITY, SUBURB, STATE, POSTCODE, COUNT from NSW_BIRTH_RATE where SUBURB = ? COLLATE NOCASE', [SUBURB])
        details = details_cur.fetchall()

        return_values = []

        for detail in details:
            detail_dict = {}
            detail_dict['YEAR'] = detail['YEAR']
            detail_dict['LOCALITY'] = detail['LOCALITY']
            detail_dict['SUBURB'] = detail['SUBURB']
            detail_dict['STATE'] = detail['STATE']
            detail_dict['POSTCODE'] = detail['POSTCODE']
            detail_dict['COUNT'] = detail['COUNT']\

            return_values.append(detail_dict)

        return make_response(jsonify(return_values), 200)

if __name__ == '__main__':
    app.run()