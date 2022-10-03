import os
import time
from paramiko.ssh_exception import SSHException, AuthenticationException
from utils.providers import ConfigProvider, SchemaProvider
from utils.save_tool import SaveTool
import paramiko
from rich import print
from utils.interface.display_handler import console

if __name__ == '__main__':
    # Display logo
    console.print("[bold blue]______          _     [bold white] _____ _               _                _       _   \n"
                  "[bold blue]|  _  \\        | |   [bold white] /  __ \\ |             | |              (_)     | |  \n"
                  "[bold blue]| | | |___  ___| | __ [bold white]| /  \\/ |__   ___  ___| | ___ __   ___  _ _ __ | |_ \n"
                  "[bold blue]| | | / _ \\/ __| |/ /[bold white] | |   | '_ \\ / _ \\/ __| |/ / '_ \\ / _ \\| | '_ \\| __|\n"
                  "[bold blue]| |/ /  __/ (__|   <  [bold white]| \\__/\\ | | |  __/ (__|   <| |_) | (_) | | | | | |_ \n"
                  "[bold blue]|___/ \\___|\\__|_|\\ [bold white]_\\  \\____/_| |_|\\___|\\___|_|\\_\\ .__/ \\___/|_|_| |_|\\__|\n"
                  "[bold blue]                      [bold white]                           | |                      \n"
                  "[bold blue]                      [bold white]                           |_|                      \n")

    with console.status("Loading configs and schemas..."):
        cp = ConfigProvider()
        cp.project_root = os.path.dirname(os.path.abspath(__file__))

        sp = SchemaProvider(config_provider=cp)

    console.print(f"Detected {cp.local_platform} as local platform")

    if "LINUX" != cp.local_platform:
        console.print("This tool is only supported on linux for now")
        exit()

    # Open a transport
    with console.status(f"Attempting to connect to your steam deck at: {cp.deck_user}@{cp.deck_host}\n"):
        connected = False

        while not connected:
            try:
                transport = paramiko.Transport((cp.deck_host, cp.deck_port))
                connected = True
                console.log(
                    f"[bold green]Connection to [bold blue]{cp.deck_host}[bold green] established!")
            except SSHException as ex:
                console.log(f"[bold red]Error: {ex.args[0]}")
            time.sleep(cp.deck_retry_auth_delay)

    # Auth
    with console.status(f"Attempting to login as: {cp.deck_user}\n"):
        try:
            transport.connect(None, cp.deck_user, cp.deck_pass)
        except AuthenticationException as ex:
            console.log(f"[bold red]Invalid username or password!\n"
                        f"Aborting!\n"
                        f"Make sure that the user and password combination in your [bold green]config.properties[bold red] file are correct!")
            exit()

    # Instantiate a SaveTool object and pass it a SFTP client and the config provider
    st = SaveTool(sftp_client=paramiko.SFTPClient.from_transport(transport), config_provider=cp, schema_provider=sp)

    with console.status("Fetching remotely installed AppIDs..."):
        st.get_installed_app_ids()
        console.log("Done fetching remote AppIDs!")

    console.log("Pulling remote saves")
    st.pull_remote_saves()

    # Close
    if st.client: st.teardown()
    if transport: transport.close()
