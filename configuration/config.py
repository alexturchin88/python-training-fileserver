import yaml
from utils.logger import logger
from vars import config_file


class Config:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Config.__instance is not None:
            raise Exception("Config class is a singleton!")
        else:
            Config.__instance = self
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
        except Exception:
            logger.critical(f"Failed to read config file '{config_file}'")
            raise
        settings = config['settings']
        self.date_format = settings['date_format']
        self.file_name_len_min = settings['file_name_len_min']
        self.file_name_len_max = settings['file_name_len_max']
