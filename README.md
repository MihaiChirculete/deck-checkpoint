![](/home/mihai/Projects/PyCharm/deck-checkpoint/DeckCheckpointPreview.png "Deck Checkpoint")  

# Deck-Checkpoint  
This is a save syncronization utility that aims to make it easy to sync saves between your steam deck and other devices.
Since some games on steam do not support cloud saves you need to manually transfer save games from
your deck to other devices. This tool takes care of that for you automatically!

# Requirements
### Remote Requirements (On Steam Deck)
 - SSH enabled (if you don't already have it enabled by now, check out this [tutorial](https://shendrick.net/Gaming/2022/05/30/sshonsteamdeck.html))

### Local Requirements
 1. [Install Python 3.9.5](https://www.python.org/downloads/release/python-395/) or newer (to check yours run `python --version`)
 2. [Create a virtual environment](https://docs.python.org/3/library/venv.html) for the project
 3. Activate your virtual environment: `source /path/to/your/venv/bin/activate`
 4. Install all the required packages in your venv: `pip install -r requirements.txt`
 5. Change the `config.properties` file according to your setup.

# Usage
This tool is designed to be run on your main computer not on your steam deck.
The idea behind is that you most likely are using your steam deck for portable gaming while also having
a main PC with keyboard, mouse and a bigger display than the deck so it's most likely easier to navigate
your main PC.  
Therefore, this tool is supposed to be run from your main PC and connect to your steam deck via SSH
to pull and push save data for your games between the two.

With that in mind, pull this project on your main PC and follow the instructions in the "Requirements" section to
have it set up. After that, simply run the **main.py** script inside the activated venv you created.

# Disclaimer
Use this tool at your own risk. This tool is under development and functionality may be missing or broken.
Always create backups of your saves to prevent loss of data.
**I am not responsible for any corrupted or lost save!**
