import yaml
import os

CONFIG_PATH = 'config/ipmonitor.local.yaml'
PACKAGE_PATH = os.path.dirname(os.path.dirname(__file__))
DEFAULT_CONFIG = os.path.join(PACKAGE_PATH, CONFIG_PATH)


class ConfigManager(object):

    def __init__(self, cfg_path=DEFAULT_CONFIG):
        # Handle NoneType cfg_path
        cfg_path = cfg_path if cfg_path else DEFAULT_CONFIG
        self.cfg = self.load_cfg(cfg_path)

    def load_cfg(self, cfg_path):
        with open(cfg_path) as f:
            return yaml.load(f)

    def get_monitors(self):
        return self.cfg.get('monitors', list())
