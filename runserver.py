from web_app import app
import os

debug = os.environ.get('DEBUG', default=False)

# TODO add args for admin and debug
app.run(host='0.0.0.0', debug=debug, threaded=True, ssl_context=('server.crt', 'server.key'))
