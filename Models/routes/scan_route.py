from flask import render_template, make_response
from flask_apispec import MethodResource


class Scan(MethodResource):

    def get(self):
        #TODO
        template = render_template('scan.html')
        response = make_response(template)
        return response