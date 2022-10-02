import json


class ParsedSchemaBase:
    def __init__(self, json_data: json):
        self.json_data = json_data
        self.schema_file = None

    def get_schema_name(self):
        return str(self.json_data["schema"]["name"])

    def get_schema_description(self):
        return str(self.json_data["schema"]["description"])


class PlatformsSchema(ParsedSchemaBase):
    def __init__(self, json_data: json):
        super().__init__(json_data)

    # TO-DO: Add schema specific methods


class GamesSchema(ParsedSchemaBase):
    def __init__(self, json_data: json):
        super().__init__(json_data)

    # TO-DO: Add schema specific methods
