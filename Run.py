import requests # For using the API
from pathlib import Path # For searching the files
from py_essentials import hashing as hs # For hashing the file (Needed by the API)
from requests.exceptions import HTTPError # Checking if something went wrong
from colorama import Fore, init # This is completely optional, you can remove it if you want to, just adds some "Spice"

Authorization = 'YOURMODRINTHAPIKEYHERE' # <---- Your modrinth api key.

init(convert=True) # For whatever reason without this colorama doesn't want to work

MCVersion = input('Minecraft version: ')  # Get the version we should update the mods to
Loader = input('Fabric or Forge?: ')  # Get the loader the mods use

#Do not touch these, unless you know what you're doing.
headers = { 'Content-Type': 'application/json',  'Authorization': Authorization }
data = { 'loaders': [Loader], 'game_versions': [MCVersion] }

#Let's go through all the files that are in the folder called "ModsFolder" and check if it's a .jar file
for txt_path in Path('ModsFolder').glob('*.jar'):
    #Let's hash the file and send a POST request to the api
    response = requests.post(
        'https://api.modrinth.com/v2/version_file/' + hs.fileChecksum(txt_path, 'sha1') + '/update?algorithm=sha1',
        json=data,
        headers=headers
    )   

    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(Fore.RED + "[X] " + Fore.RESET + "Mod not found: " + Fore.LIGHTBLUE_EX + '"' + str(txt_path) + '" ' + Fore.RESET + "was not found in modrinth or not updated to the version " + Fore.LIGHTBLUE_EX + MCVersion + Fore.RESET + ", if it is then you'll have to manually download it.")
    except Exception as err:
        print(f'{err}')
    else: ## Success!
        responsejson = response.json()
        print(Fore.LIGHTGREEN_EX + "[+] " + Fore.RESET + 'Downloading mod: ' + Fore.LIGHTBLUE_EX + responsejson["files"][0]["filename"] + '...' + Fore.RESET)
        r = requests.get(responsejson["files"][0]["url"], allow_redirects=True) # Gets the download url
        open('NewMods/' + responsejson["files"][0]["filename"], 'wb').write(r.content) # Downloads the new mod.