import sys
from app import create_app  # Replace 'your_app_module' with the actual module name of your Flask app

# If debugging is not enabled, run the app using Gunicorn
from gunicorn.app.wsgiapp import WSGIApplication

if __name__ == '__main__':
    app = create_app()

    gunicorn_app = WSGIApplication()
    gunicorn_app.app_uri = 'app:create_app()'  # Replace 'your_app_module' with your actual app module

    # You can specify Gunicorn options here if needed, such as number of workers, bind address, etc.
    gunicorn_options = {
        'bind': '192.168.1.240:8000',  # Change the bind address and port as needed
        'workers': 4,  # You can adjust the number of worker processes
    }

    # gunicorn_options = {
    #    'bind': 'mydomainname.com:443',
    #     'workers': 4,
    #     'keyfile': '/path/to/your/private/key.pem',  # Path to your SSL private key
    #     'certfile': '/path/to/your/certificate.crt',  # Path to your SSL certificate
    # }

    # Run Gunicorn with the specified options
    gunicorn_app.run(**gunicorn_options)
