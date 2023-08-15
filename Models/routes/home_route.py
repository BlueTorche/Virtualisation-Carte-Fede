
from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies

from Models.database.databasemodels import User
from Models.utils.limiter import limiter


class Home(MethodResource):
    decorators = [limiter.limit("10/minute")]  # Apply rate limiting to the class

    def post(self):
        return

    def get(self):
        user = User.query.filter_by(user_email="default@admin.com").first()
        message =user.user_id

        template = render_template('home.html', message=message)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response

def render_php_template(template_name):
    # Read the contents of the PHP template file
    with open(template_name, 'r') as template_file:
        template_content = template_file.read()

    # You may need to install a PHP interpreter library (e.g., `php` command) and use it here to render the PHP content.
    # Example: php_rendered_content = php_interpreter.render(template_content)

    # For demonstration purposes, let's assume the PHP rendering library is called `php_renderer`
    php_rendered_content = php_renderer.render(template_content)

    return php_rendered_content