from flask import render_template, make_response
from flask_apispec import MethodResource


class View(MethodResource):

    def get(self):
        # TODO
        template = render_template('view.html')
        response = make_response(template)
        return response