import os
import pwd
import time
from typing import List
import stat
import errno
from paramiko import SFTPClient
from utils.providers import ConfigProvider, SchemaProvider
from utils.interface.display_handler import console


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

    def pull_remote_saves(self):
        """
        Pulls remote saves based on defined schemas
        :return:
        """
        if len(self.remote_appids) < 1:
            return 1

        gs = self.sp.get_games_schema()
        ps = self.sp.get_platforms_schema()

        with console.pager():
            for app_id in self.remote_appids:
                # Search the games schema for this appId
                game_schema = gs.get_schema_for_app_id(app_id)
                console.rule(f"[bold magenta]Sync-ing save data for [blue]{gs.get_name_for_app_id(app_id)} (AppID {app_id})...")


                if game_schema:
                    console.log(f"[bold green]Found schema for app_id [blue]{app_id}[green]!\n"
                                  f"Game identified as [blue]{gs.get_name_for_app_id(app_id)}")

                    remote_saves = [ps.get_saves_root_for_platform("LINUX") \
                                        .replace("{user}", self.cp.deck_user) \
                                        .replace("{app_id}", app_id) + savePath for savePath in
                                    gs.get_save_paths_for_app_id(app_id)]

                    local_saves = [ps.get_saves_root_for_platform(self.cp.local_platform) \
                                       .replace("{user}", pwd.getpwuid(os.getuid())[0]) \
                                       .replace("{app_id}", app_id) + savePath for savePath in
                                   gs.get_save_paths_for_app_id(app_id)]

                    save_pairs = list(zip(remote_saves, local_saves))

                    for save_pair in save_pairs:
                        self.pull_save_files(save_pair[0], save_pair[1])

                else:
                    console.log(f"[bold yellow]Unable to identify app_id [blue]{app_id}!\n"
                                f"[yellow]Falling back to UNIDENTIFIED_GAME_SCHEMA")

        return 0

    def pull_save_files(self, remote_path, local_path):
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        for filename in self.client.listdir(remote_path):
            if stat.S_ISDIR(self.client.stat(remote_path + filename).st_mode):
                # uses '/' path delimiter for remote server
                self.pull_save_files(remote_path + filename + '/', os.path.join(local_path, filename))
            else:
                if not os.path.isfile(os.path.join(local_path, filename)) or self.client.stat(
                        remote_path + filename).st_mtime > os.path.getmtime(os.path.join(local_path, filename)):
                    console.log(
                        f"[bold green]Remote file {remote_path + filename} is newer than local file {os.path.join(local_path, filename)}, pulling from remote...")
                    self.client.get(remote_path + filename, os.path.join(local_path, filename))
                else:
                    console.log(
                        f"[bold yellow]Remote file {remote_path + filename} is older than local file {os.path.join(local_path, filename)}, keeping local file...")

    def push_save_file(self, local_path, remote_path):
        self.client.put(local_path, remote_path)

    def teardown(self):
        self.client.close()
