import os
from configparser import ConfigParser
import platform


class ConfigProvider:
    def __init__(self):
        config = ConfigParser()
        config.read("config.properties")

        self.local_platform = str(platform.system()).upper()

        self.auto_pull_saves = bool(config.get("AppSettings", "checkpoint.automatically_pull_all_saves"))

        self.deck_host = str(config.get("SSH-Section", "deck.host"))
        self.deck_port = int(config.get("SSH-Section", "deck.port"))
        self.deck_user = str(config.get("SSH-Section", "deck.user"))
        self.deck_pass = str(config.get("SSH-Section", "deck.password"))
        self.deck_reconnect_delay = int(config.get("SSH-Section", "deck.reconnect_delay"))