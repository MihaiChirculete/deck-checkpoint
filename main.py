import os

from utils.providers import ConfigProvider, SchemaProvider
from utils.save_tool import SaveTool
import paramiko

if __name__ == '__main__':
    cp = ConfigProvider()
    cp.project_root = os.path.dirname(os.path.abspath(__file__))

    sp = SchemaProvider(config_provider=cp)

    print(cp.local_platform)

    if "LINUX" != cp.local_platform:
        print("This tool is only supported on linux for now")
        exit()

    # Open a transport
    print(f"Attempting to connect to your steam deck at: {cp.deck_user}@{cp.deck_host}")
    transport = paramiko.Transport((cp.deck_host, cp.deck_port))

    # Auth
    print(f"Attempting to authenticate on Steam Deck as '{cp.deck_user}'")
    transport.connect(None, cp.deck_user, cp.deck_pass)

    # Instantiate a SaveTool object and pass it a SFTP client and the config provider
    st = SaveTool(sftp_client=paramiko.SFTPClient.from_transport(transport), config_provider=cp, schema_provider=sp)
    st.get_installed_app_ids()
    st.pull_remote_saves()

    # Close
    if st.client: st.teardown()
    if transport: transport.close()
