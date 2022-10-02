from typing import List

from paramiko import SFTPClient
from utils.providers import ConfigProvider, SchemaProvider


class SaveTool:
    remote_appids: list[str]

    def __init__(self, sftp_client: SFTPClient, config_provider: ConfigProvider, schema_provider: SchemaProvider):
        self.client = sftp_client
        self.cp = config_provider
        self.sp = schema_provider
        self.remote_appids = None

    def get_installed_app_ids(self):
        self.remote_appids = self.client.listdir(f"/home/{self.cp.deck_user}/.steam/root/steamapps/compatdata/")
        return self.remote_appids

    def prepare_local_structure(self):
        """
        Prepares local directories corresponding to remote ones.
        :return:
        """
        if len(self.remote_appids) < 1:
            return 1

        games_schema = self.sp.get_games_schema()["games"]

        for app_id in self.remote_appids:
            found_schema = False
            # Search the games schema for this appId
            for game in games_schema:
                if game["appId"] == str(app_id):
                    found_schema = True
                    print(f"Found schema for app_id {app_id}! Game identified as {game['gameName']}")
                    break

            if found_schema is False:
                print(f"Unable to identify app_id {app_id}! Falling back to {games_schema[0]['gameName']}")

        return 0

    def pull_save_file(self, remote_path, local_path):
        self.client.get(remote_path, local_path)

    def push_save_file(self, local_path, remote_path):
        self.client.put(local_path, remote_path)

    def teardown(self):
        self.client.close()
