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
            if platform == platform_name:
                return platform

        return None

    def get_saves_root_for_platform(self, platform_name: str):
        return str(self.get_schema_for_platform(platform_name=platform_name)["savesRoot"])


class GamesSchema(ParsedSchemaBase):
    def __init__(self, json_data: json):
        super().__init__(json_data)

    # TO-DO: Add schema specific methods
