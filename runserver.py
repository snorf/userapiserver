from userapiserver import app, setup_database
import os

if __name__ == '__main__':
    if not os.path.isfile(app.config['SQLALCHEMY_DATABASE_URI']):
      setup_database(app)
    context = ('cert.crt', 'key.key')
    app.run(host='0.0.0.0', port=8443, ssl_context=context, threaded=True, debug=False)
