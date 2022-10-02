import json


class ParsedSchemaBase:
    def __init__(self, json_data: json):
        self.json_data = json_data
        self.schema_file = None

    def get_json(self):
        return self.json_data

    def get_schema_name(self):
        return str(self.json_data["schema"]["name"])

    def get_schema_description(self):
        return str(self.json_data["schema"]["description"])


class PlatformsSchema(ParsedSchemaBase):
    def __init__(self, json_data: json):
        super().__init__(json_data)

    def get_schema_for_platform(self, platform_name: str):
        platform_name = platform_name.upper()

        for platform in self.json_data["platforms"]:
            if platform["platform"] == platform_name:
                return platform
        return None

    def get_saves_root_for_platform(self, platform_name: str):
        return str(self.get_schema_for_platform(platform_name=platform_name)["savesRoot"])


class GamesSchema(ParsedSchemaBase):
    def __init__(self, json_data: json):
        super().__init__(json_data)

    def get_schema_for_app_id(self, app_id: str):
        for game in self.json_data["games"]:
            if game["appId"] == app_id:
                return game
        return None

    def get_schema_for_game_name(self, game_name: str):
        for game in self.json_data["games"]:
            if game["gameName"] == game_name:
                return game
        return None

    def get_save_paths_for_app_id(self, app_id: str):
        return self.get_schema_for_app_id(app_id)["savePaths"]

    def get_save_paths_for_game_name(self, game_name: str):
        return self.get_schema_for_game_name(game_name)["savePaths"]

    def get_excluded_save_paths_for_app_id(self, app_id: str):
        return self.get_schema_for_app_id(app_id)["excludedSavePaths"]

    def get_excluded_save_paths_for_game_name(self, game_name: str):
        return self.get_schema_for_game_name(game_name)["excludedSavePaths"]

    def get_name_for_app_id(self, app_id: str):
        return self.get_schema_for_app_id(app_id)["gameName"]

    def get_app_id_for_name(self, game_name: str):
        return self.get_schema_for_game_name(game_name)["appId"]