from app import create_app, sio
from config import Config

app = create_app()

if __name__ == '__main__':
    sio.run(app, host=Config.IP_ADDRESS, port=Config.PORT, debug=Config.DEBUG)
    app.app_context().pop('app.models')
