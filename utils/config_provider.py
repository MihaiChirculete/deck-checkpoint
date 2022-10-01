import os
from configparser import ConfigParser
import platform

class ConfigProvider:
    def __init__(self):
        config = ConfigParser()
        config.read("config.properties")

        self.local_platform = str(platform.system()).upper()

        self.local_saves_dir = str(config.get("AppSettings", "checkpoint.saves_dir"))

        self.deck_host = str(config.get("SSH-Section", "deck.host"))
        self.deck_port = int(config.get("SSH-Section", "deck.port"))
        self.deck_user = str(config.get("SSH-Section", "deck.user"))
        self.deck_pass = str(config.get("SSH-Section", "deck.password"))
        self.deck_reconnect_delay = int(config.get("SSH-Section", "deck.reconnect_delay"))

        # Call the setup in order to make sure all required dirs are created and up to date with the config
        self.setup()

    def setup(self):
        # Check if the local saves dir exists and create it otherwise
        if not os.path.isdir(self.local_saves_dir):
            print(f"Saves dir doesn't exist, creating it at: {self.local_saves_dir}")
            os.makedirs(self.local_saves_dir)