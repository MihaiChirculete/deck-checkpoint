import json
import os
from configparser import ConfigParser
from utils.data_types.parsed_schemas import PlatformsSchema, GamesSchema
import platform


class ConfigProvider:
    def __init__(self):
        config = ConfigParser()
        config.read("config.properties")

        # This will actually be set in the main.py script
        self.project_root = None
        self.local_platform = str(platform.system()).upper()

        self.auto_pull_saves = bool(config.get("AppSettings", "checkpoint.automatically_pull_all_saves"))

        self.deck_host = str(config.get("SSH-Section", "deck.host"))
        self.deck_port = int(config.get("SSH-Section", "deck.port"))
        self.deck_user = str(config.get("SSH-Section", "deck.user"))
        self.deck_pass = str(config.get("SSH-Section", "deck.password"))
        self.deck_reconnect_delay = int(config.get("SSH-Section", "deck.reconnect_delay"))


class SchemaProvider:
    def __init__(self, config_provider: ConfigProvider):
        self.cp = config_provider
        self.platforms_schema = PlatformsSchema(json_data=json.load(open(self.cp.project_root + "/schemas/platforms.json")))
        self.games_schema = GamesSchema(json_data=json.load(open(self.cp.project_root + "/schemas/games.json")))

    def get_platforms_schema(self):
        return self.platforms_schema.get_json()

    def get_games_schema(self):
        return self.games_schema.get_json()