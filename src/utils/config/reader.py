import yaml
import os

class ConfigFileReader:
    """
    Reads configuration from config.yaml in the project root.
    """
    
    _CONFIG_FILE = "config.yaml"

    @staticmethod
    def get_strategy_name() -> str:
        """
        Retrieves the strategy identifier from the config file.
        """
        with open(ConfigFileReader._CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
            return config["strategy"]
