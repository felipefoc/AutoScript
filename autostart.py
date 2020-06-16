###############################################################################
# League of Legends (LCU API) script
#
# Auto accept matchmaking
# Automatic/instant pick champion
# Automatic/instant lock champion
# Set High process priority
#
# Usage:
# python lcu-mm-auto-accept-auto-lock-champion.py "Jax" "Xayah"
#
# Edit the "championsPrio" list below to the champions you want.
# Champion names passed as arguments get highest priority.
#
# Built on Python 3.x
# Dependencies: requests, colorama


def autostart():
    import requests
    import urllib3
    import playsound
    from base64 import b64encode
    from time import sleep
    import os
    from colorama import Style

    #############################################################################################################
    #  Resource para o PyInstaller
    def resource_path(relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Audios do Playsound
    audio = (resource_path('audio/rick_astley.wav'))

    # Set to your game directory (where LeagueClient.exe is)
    gamedirs = [r'C:\Riot Games\League of Legends']

    # Set to True to stop script when match starts
    stopWhenMatchStarts = True

    ###############################################################################
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Helper function
    def request(method, path, query='', data=''):  # Estudar que porra é essa
        if not query:
            url = '%s://%s:%s%s' % (protocol, host, port, path)
        else:
            url = '%s://%s:%s%s?%s' % (protocol, host, port, path, query)

        print('%s %s %s' % (method.upper().ljust(7, ' '), url, data))
        # print(Back.BLACK + Fore.YELLOW + method.upper().ljust(7, ' ') + Style.RESET_ALL + ' ' + url + ' ' + data)

        fn = getattr(s, method)

        if not data:
            r = fn(url, verify=False, headers=headers)
        else:
            r = fn(url, verify=False, headers=headers, json=data)

        return r

    ###
    # Read the lock file to retrieve LCU API credentials
    #

    lockfile = None
    print('Waiting for League of Legends to start ..')

    # Validate path / check that Launcher is started

    while lockfile is None:
        try:
            for gamedir in gamedirs:
                lockpath = r'%s\lockfile' % gamedir

                if not os.path.isfile(lockpath):
                    print('League of legends not in execute.')
                    sleep(2)

                if os.path.isfile(lockpath):
                    print('Found running League of Legends, dir', gamedir)
                    sleep(5)
                    lockfile = open(r'%s\lockfile' % gamedir, 'r')

        except FileNotFoundError:
            sleep(1)

    # Read the lock file data
    lockdata = lockfile.read()
    print(lockdata)
    lockfile.close()

    # Parse the lock data
    lock = lockdata.split(':')

    procname = lock[0]
    pid = lock[1]

    protocol = lock[4]
    host = '127.0.0.1'
    port = lock[2]

    username = 'riot'
    password = lock[3]

    ###
    # Prepare Requests
    #

    # Prepare basic authorization header
    userpass = b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')
    headers = {'Authorization': 'Basic %s' % userpass}
    print(headers['Authorization'])

    # Create Request session
    s = requests.session()

    ###
    # Wait for login
    #

    # Check if logged in, if not then Wait for login
    while True:
        try:
            sleep(1)
            r = request('get', '/lol-login/v1/session')

            if r.status_code != 200:
                print(r.status_code)
                continue

            # Login completed, now we can get data
            if r.json()['state'] == 'SUCCEEDED':
                break
            else:
                print(r.json()['state'])

        except ConnectionRefusedError:
            sleep(1)

    while True:
        r = request('get', '/lol-gameflow/v1/gameflow-phase')  # None/Lobby/MatchMaking

        if r.status_code != 200:
            print(str(r.status_code) + Style.RESET_ALL, r.text)
            continue
        print(str(r.status_code) + Style.RESET_ALL, r.text)

        phase = r.json()

        # Auto accept match
        if phase == 'ReadyCheck':
            request('post', '/lol-matchmaking/v1/ready-check/accept')
            playsound.playsound(audio, False)
            sleep(7)


        elif phase == 'InProgress':
            print('Game em andamento.')

            if stopWhenMatchStarts:
                break
            else:
                sleep(9)
        sleep(1)



