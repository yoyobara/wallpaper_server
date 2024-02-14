import flask
import pathlib
import random
import os
import platformdirs
import tomllib

DATA_DIR = platformdirs.user_data_dir("wpserver")
CONFIG_FILE = os.path.join(DATA_DIR, 'config.toml')

# will be overriden by custom toml
config = {
    'HOSTNAME': '0.0.0.0',
    'PORT': 8000,
    'SET_WP_CMD': 'set_wallpaper'
}

def set_wallpaper_to_desktop(uri: str):
    os.system(f"{config['SET_WP_CMD']} {uri}")

class WallpaperManager:
    WALLPAPERS_DIR = os.path.join(DATA_DIR, 'wallpapers')

    def __init__(self) -> None:

        if not os.path.exists(self.WALLPAPERS_DIR):
            os.makedirs(self.WALLPAPERS_DIR, exist_ok=True)

        self.wallpapers: set = set()
        self.load_wallpapers()

    def load_wallpapers(self):
        if not os.path.exists(self.WALLPAPERS_DIR):
            os.mkdir(self.WALLPAPERS_DIR)

        self.wallpapers.update(os.listdir(self.WALLPAPERS_DIR))

    def get_random_wallpaper_uri(self) -> str | None:
        if not self.wallpapers:
            return None

        wp = random.choice(list(self.wallpapers))
        return pathlib.Path(self.WALLPAPERS_DIR, wp).as_uri()


app = flask.Flask(__name__)
manager = WallpaperManager()



@app.route('/set_random', methods=['POST'])
def set_random():
    rnd_uri = manager.get_random_wallpaper_uri()

    if rnd_uri is None:
        return flask.jsonify(success=False, uri=None)
    else:
        set_wallpaper_to_desktop(rnd_uri)
        return flask.jsonify(success=True, uri=rnd_uri)

def main():
    # override default config with user specifics
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            toml_conf = tomllib.load(f)
            config.update(toml_conf)

    # run application
    app.run(config['HOSTNAME'], config['PORT'])

if __name__ == "__main__":
    main()
