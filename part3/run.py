from app import create_app
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
}

config_class = config_map.get(os.getenv('FLASK_ENV', 'development'), DevelopmentConfig)
app = create_app(config_class)

if __name__ == '__main__':
    app.run(debug=True)
