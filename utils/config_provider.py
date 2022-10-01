from configparser import ConfigParser


class ConfigProvider:
    def __init__(self):
        config = ConfigParser()
        config.read("config.properties")

        self.deck_user = str(config.get("SSH-Section", "deck.user"))
        self.deck_pass = str(config.get("SSH-Section", "deck.password"))
        self.deck_reconnect_delay = int(config.get("SSH-Section", "deck.reconnect_delay"))