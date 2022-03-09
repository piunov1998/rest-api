from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg2
from contextlib import closing
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
api = Api(app)

"""
If you want to launch rest-service with out data it's nessary to change this variables
"""

# database host
host = 'localhost'
# database name
dbname = 'orbis'
# username who has acces to db
user = 'user'
# password of this user
password = '0000'


class Rest_API(Resource):
    """"
    Represents rest-service class with GET method
    """

    def get_items(self, id: int=0, filter: str='%') -> dict:
        """Makes SELECT request to database"""
        if filter != '%':
            filter = '%' + filter + '%'
        with closing(psycopg2.connect(dbname=dbname, user=user, password=password, host=host)) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    'SELECT name, type FROM objects WHERE (id = %s OR parent_id = %s) AND name ilike %s ORDER BY id', (id, id, filter)
                    )
                return cursor.fetchall()

    def get(self, id: int=0):
        """Represens GET method responcer. It parses arguments and invoke get_items() with them"""
        arg_parser = reqparse.RequestParser()
        arg_parser.add_argument('filter', default='%', type=str)
        args = arg_parser.parse_args()
        filter = args['filter']
        if not str(id).isnumeric():
            return 'Wrong value', 400
        else:
            try:
                items = self.get_items(id, filter)
            except Exception as error:
                print('\nError:\n', error, type(error), '\n')
                return 'Error', 500
            if items:
                return items, 200
            else:
                return 'Not found', 404


api.add_resource(Rest_API, '/object', '/object/', '/object/<int:id>')

if __name__ == '__main__':
    app.run(debug=False, port=80)