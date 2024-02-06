import flask
import os
import platformdirs
import tomllib

DATA_DIR = platformdirs.user_data_dir("wpserver")
CONFIG_FILE = os.path.join(DATA_DIR, 'config.toml')

app = flask.Flask(__name__)

def main():
    config = {
        'HOSTNAME': '0.0.0.0',
        'PORT': 8000,
        'SET_WP_CMD': 'echo "change me in config.toml"'
    }

    # override default config with user specifics
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            toml_conf = tomllib.load(f)
            config.update(toml_conf)

    # run application
    app.run(config['HOSTNAME'], config['PORT'])

