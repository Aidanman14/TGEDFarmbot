'''
    Hi, I am not familiar with OOP yet, therefore you'll have to stick with this shitty code, sorry!

    Farmbot version: 1.0.4
    Made by: Aidanman14/RiceEaten

    Thank you for using this farmbot!
'''

### Imports
import requests
import json
import time
import os
import uuid

### Variables
farmBotVersion = "1.0.4"
gameBuild = ""

global tokens
tokens = {}

scriptDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(scriptDir, "tokens.txt")
folderPath = os.path.join(scriptDir, "tokensStorage")

def getGameInfo():
    specialHeaders = {
        'Host': 'tino.detailgames.ai',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
        'Accept-Language': 'en-GB,en;q=0.9',
        'X-Unity-Version': '2022.3.62f2',
    }

    response = requests.get('https://tino.detailgames.ai/games/1/status', headers=specialHeaders)
    responseJson = json.loads(response.text) 
    return (responseJson["status"], responseJson["version"])

# Refreshes & gets new tokens from the game's server
def getNewPlayerTokens():
    specialHeaders = {
        'Host': 'tino.detailgames.ai',
        'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
        'x-client-build': gameBuild,
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Authorization': 'Bearer ',
        'X-Unity-Version': '2022.3.62f2',
        'Content-Type': 'application/json',
    }

    json_data = {
        'refreshToken': tokens["refreshToken"],
    }

    response = requests.post('https://tino.detailgames.ai/auth/refresh', headers=specialHeaders, json=json_data)
    #print(response.text)
    return json.loads(response.text)

# Test if the player's tokens are valid
def testPlayerTokens():
    response = requests.get('https://tino.detailgames.ai/users/me', headers=headersGet)
    #print(response.text)
    if response.status_code == 400 or response.status_code == 401:
        return False
    return True

# Get the player's details: username, level & current stage they're on
def getPlayerDetails():
    playerData1 = json.loads(requests.get('https://tino.detailgames.ai/users/me', headers=headersGet).text)
    playerData2 = json.loads(requests.get('https://tino.detailgames.ai/tged/account', headers=headersGet).text)

    return (playerData1["nickname"], playerData2["level"], playerData2["stageSummary"]["maxStage"])

def getBattlepasses():
    response = requests.get('https://tino.detailgames.ai/tged/liveops/battlepass', headers=headersPostJson)
    passesData = json.loads(response.text)["passes"]
    passes = []
    for _pass in passesData:
        passes.append((_pass["id"], _pass["currentIndex"], _pass["maxIndex"]))
    
    return passes
    
# Very bad auto farming subprogram, VERY VERY scuffed.
def farmStages(stages):
    global maxCurrentStage
    if (stages == 0):
        stages = 99999999999999 # lol
    for stage in range(maxCurrentStage, maxCurrentStage + stages):
        try:
            waves = 20

            if stage % 5 == 0:
                waves = 30
            
            if stage == 0:
                waves = 10

            # Start stage
            json_data = {
                'stage': stage,
                'deployedCharacters': [
                    4007,
                    4010,
                    4001,
                    4006,
                ],
            }
            response = requests.post('https://tino.detailgames.ai/tged/stages/start', headers=headersPostJson, json=json_data)

            #print(response.text)

            # Gets the session ID of the stage
            responseJson = json.loads(response.text)
            sessionId = ""
            if (not responseJson["sessionId"]):
                print("Session Id not found - You might be out of energy!")
                input("Press enter to continue.")
                return
                #quit()

            sessionId = responseJson["sessionId"]

            print(f"Started stage session ({sessionId}) for stage {stage}")

            json_data = {
                'stage': stage,
                'wave': waves,
                'clearTime': 41207,
            }

            response = requests.post(
                'https://tino.detailgames.ai/tged/leaderboard/stages/realtime-rank',
                headers=headersPostJson,
                json=json_data,
            )
            #print(response.text)

            json_data = {
                'sessionId': sessionId,
                'stage': stage,
                'wave': waves,
                'clearTime': 358886,
                'missionId': 0,
                'characterDamages': [
                    {
                        'characterId': '4010',
                        'totalDamage': '18893266',
                    },
                    {
                        'characterId': '4001',
                        'totalDamage': '22642928',
                    },
                    {
                        'characterId': '4007',
                        'totalDamage': '30343078',
                    },
                    {
                        'characterId': '4006',
                        'totalDamage': '32664713',
                    },
                ],
            }

            response = requests.post('https://tino.detailgames.ai/tged/stages/end', headers=headersPostJson, json=json_data)

            #print(response.text)

            responseJson = json.loads(response.text)

            if (not responseJson["stageSummary"]):
                print("An error occured")
                input("Press enter to continue.")
                return
                #quit()
            
            print(f"Stage {stage} completed.")
            maxCurrentStage += 1

            time.sleep(.5)
        except KeyboardInterrupt:
            print("Interrupted.")
            return
        except:
            print("Energy depleted OR unknown error.")
            return

# Very bad auto summoning subprogram
def autoSummon(times, exclusive):
    if (times == 0):
        times = 9999999999
    for i in range(1, times+1):
        try:
            json_data = {
                'count': 10,
                'isExclusive': exclusive,
            }
            response = requests.post('https://tino.detailgames.ai/tged/gacha/56000/draw', headers=headersPostJson, json=json_data)

            #print(response.text)

            if "success" in response.text:
                print(f"Summon success ({i})")
            else:
                print("Tickets depleted OR unknown error.")
                return

            time.sleep(.5)
        except KeyboardInterrupt:
            print("Interrupted.")
            return
        except:
            print("Tickets depleted OR unknown error.")
            return

def completeBP(passId, max):
    try:
        print(passId)
        json_data = {
            'missions': [
                {
                    'id': int(passId),
                    'missionIndex': int(max), # just to make sure it's the correct type
                },
            ],
        }

        response = requests.post(
            'https://tino.detailgames.ai/tged/liveops/battlepass/clear-mission',
            headers=headersPostJson,
            json=json_data,
        )

        #print(response.text)

        if response.status_code == 400:
            return False
        return True
    
    except Exception as e:
        print(e)

# As name suggests.
def completeTutorial():
    json_data = {
        'step': 3,
        'isCompleted': True,
    }

    response = requests.put('https://tino.detailgames.ai/tged/account/tutorial', headers=headersPostJson, json=json_data)

    if response.status_code == 400:
        return False
    return True

# Sign up for guest accounts - good for rerolling.
def signUpGuest():
    headers = {
        'Host': 'tino.detailgames.ai',
        'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
        'Connection': 'keep-alive',
        'x-client-build': '1.0.4',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'X-Unity-Version': '2022.3.62f2',
        'Content-Type': 'application/json',
    }

    json_data = {
        'gameId': 1,
        'deviceId': str(uuid.uuid4()), # Generate a fake deviceId - not sure if it is a HWID
    }

    response = requests.post('https://tino.detailgames.ai/auth/guest/login', headers=headers, json=json_data)
    print(response.text)
    if response.status_code == 400:
        return (False, None)
    return (True, json.loads(response.text))

# Generate a simple option choosing interface, then return the user's choice
def startOptions(options):
    if (len(options) == 0):
        return 
    for i in range(0, len(options)):
        print(f"[{i+1}] {options[i]}")
    validInput = False
    userInput = ""
    while (not validInput):
        userInput = input(">> ")
        try:
            userInput = options[int(userInput)-1]
            validInput = True
        except:
            print("Invalid option.")
    return userInput

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
  time.sleep(1)

def farmStagesMenu():
    a = True
    while (a):
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Farm X number of stages", "Farm until energy depletion", "Back"])
        if (option == "Farm X number of stages"):
            X = int(input("Amount of stages to farm: "))
            farmStages(X)
            continue
        elif (option == "Farm until energy depletion"):
            farmStages(0)
            continue
        elif (option == "Back"):
            a = False

def summonMenu():
    a = True
    while (a):
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Summon normal X amount of times", "Summon normal until ticket depletion", "Summon exclusive X amount of times", "Summon exclusive until ticket depletion", "Back"])
        if (option == "Summon normal X amount of times"):
            X = int(input("Amount to summon: "))
            autoSummon(X, True)
            continue
        elif (option == "Summon exclusive X amount of times"):
            X = int(input("Amount to summon: "))
            autoSummon(X, False)
            continue
        elif (option == "Summon normal until ticket depletion"):
            autoSummon(0, True)
            continue
        elif (option == "Summon exclusive until ticket depletion"):
            autoSummon(0, False)
            continue
        elif (option == "Back"):
            a = False

def battlePassMenu():
    a = True
    while (a):
        print("Getting battlepass data...")
        passes = getBattlepasses()
        print(f"There are {len(passes)} battlepass(es) active.")
        X = []
        for _pass in passes:
            passId, progress, max = _pass
            X.append(passId)
            print(f"Battlepass ID: {passId} | Progress: {progress}, | Max level: {max}")

        option = startOptions(["Complete battlepass", "Back"])
        if (option == "Complete battlepass"):
            print("Which one to complete?")
            option2 = startOptions(X)
            if (option2 in X):
                #print(option2)
                success = completeBP(option2, max)
                if (success):
                    print("Completed battlepass.")
                else:
                    print("Could not complete battlepass.")
            continue
        elif (option == "Back"):
            a = False

# There isn't actually an api for "logging out"
def logout():
    print("Bye bye!")
    quit()

def login():
    a = True
    while (a):
        global tokens
        option = startOptions(["Log in using tokens.txt", "Log in using saved token in tokenStorage", "Return"])
        if (option == "Log in using tokens.txt"):
            with open(path, "r+") as tokensFile:
                content = tokensFile.read().strip()
                if content:
                    tokens = json.loads(content)
                    mainProgram()
                    
                else:
                    print("tokens.txt is empty!\nPlease follow the tutorial on GitHub on how to get your tokens!")
                    input("Press enter to continue...")
                    quit()
            continue
        elif (option == "Log in using saved token in tokenStorage"):
            X = []
            for name in os.listdir(folderPath):
                X.append(name)
                
            option2 = startOptions(X)
            if (option2 in X):
                with open(os.path.join(folderPath, f"{option2}"), "r+") as tokensFile:
                    content = tokensFile.read().strip()
                    if content:
                        #global tokens
                        tokens = json.loads(content)
                        #print(tokens)
                        path = os.path.join(folderPath, f"{option2}")
                        print(path)
                        mainProgram()
                    else:
                        print(f"{option2} is empty!")
                        input("Press enter to continue...")
                        quit()
            continue
        elif (option == "Return"):
            a = False
    
        clear()

def signUp():
    try:
        clear()
        print("WARNING: There isn't actually a way to sign in to these account ingame right now, but you can use the farmbot with them.")
        #print("WARNING: These tokens have an expiry date of ~5 days, please use the farmbot within that timeframe to retain access to the account.") THIS IS WRONG, ONLY THE AUTH TOKEN LASTS 5 DAYS
        print("WARNING: These tokens have an expiry time of 15 minutes, please use the farmbot within that timeframe to retain access to the account.") # REFRESH TOKEN LASTS 15 MINUTES
        input("Press enter to contiunue...")

        print("Creating account...")
        global tokens
        success, tokens = signUpGuest()
        if (not success):
            print("Account creation unsuccessful, please re-launch the farmbot.")
            input("Press enter to contiunue...")
            quit()
            
        print("Successfully created new account!")

        # Set the headers
        global headersGet, headersPostJson
        headersGet = {
                'Host': 'tino.detailgames.ai',
                'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
                'Connection': 'keep-alive',
                'x-client-build': gameBuild,
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Authorization': 'Bearer ' + tokens['accessToken'],
                'X-Unity-Version': '2022.3.62f2',
            }
        headersPostJson = {
                'Host': 'tino.detailgames.ai',
                'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
                'x-client-build': gameBuild,
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Authorization': 'Bearer ' + tokens['accessToken'],
                'X-Unity-Version': '2022.3.62f2',
                'Content-Type': 'application/json',
            }

        print("Completing tutorial...")
        completeTutorial()

        saveName = input("Enter a save name: ")
        with open(os.path.join(folderPath, f"{saveName}.txt"), "w") as f:
                print("Saving account tokens...")
                f.write(json.dumps(tokens))

        global path
        path = os.path.join(folderPath, f"{saveName}.txt")
        clear()
        mainProgram()
    except Exception as e:
        print(e)

# Main menu subprogram
def mainMenu():
    a = True
    while (a):
        global nickname, level, maxCurrentStage
        nickname, level, maxCurrentStage = getPlayerDetails()

        print(f"Username: {nickname}")
        print(f"Level: {level}")
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Farm stages", "Summon", "Battlepass", "Logout"])
        if (option == "Farm stages"):
            farmStagesMenu()
            continue
        elif (option == "Summon"):
            summonMenu()
            continue 
        elif (option == "Battlepass"):
            battlePassMenu()
            continue 
        elif (option == "Logout"):
            a = False

        clear()

def startUpMenu():
    a = True
    while (a):
        option = startOptions(["Log in to an account", "Create a new account", "Quit"])
        if (option == "Log in to an account"):
            login()
            continue
        elif (option == "Create a new account"):
            signUp()
            continue 
        elif (option == "Quit"):
            a = False
            logout()
        clear()

# Using try: except: to ignore annoying errors (i cannot be asked to fix em)
def mainProgram():
    try:
        # Generate new tokens for the player & saves them to a text file
        tokens = getNewPlayerTokens()

        #print(tokens)

        with open(path, "w") as tokensFile:
            tokensFile.write(json.dumps(tokens))
            tokensFile.close()

        # Set the headers
        global headersGet, headersPostJson
        headersGet = {
                'Host': 'tino.detailgames.ai',
                'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
                'Connection': 'keep-alive',
                'x-client-build': gameBuild,
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Authorization': 'Bearer ' + tokens['accessToken'],
                'X-Unity-Version': '2022.3.62f2',
            }
        headersPostJson = {
                'Host': 'tino.detailgames.ai',
                'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
                'x-client-build': gameBuild,
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Authorization': 'Bearer ' + tokens['accessToken'],
                'X-Unity-Version': '2022.3.62f2',
                'Content-Type': 'application/json',
            }

        if testPlayerTokens():
            print("Tokens are valid, starting farmbot.")
        else:
            print("Tokens are invalid, if this account was created using the farmbot, you've lost it forever!")
        time.sleep(1.5)

        global nickname, level, maxCurrentStage
        nickname, level, maxCurrentStage = getPlayerDetails()
        mainMenu()
    except KeyboardInterrupt:
        print("Interrupted.")
    except Exception as error:
        print(f"An error occured: {error}")

# Checks if files are in the directory
def checkFiles():
    folderMissing = False
    fileMissing = False

    if not os.path.exists(folderPath):
        folderMissing = True
    if not os.path.exists(path):
        fileMissing = True

    if folderMissing:
        os.makedirs(folderPath, exist_ok=True)
        print("tokensStorage was missing, creating file.")

    if fileMissing:
        with open(path, "w") as f:
            print("tokens.txt was missing, creating file.")
            f.write("{}")

    if folderMissing or fileMissing:
        input("Please re-launch the farmbot!\nPress enter to continue...")
        quit()
    else:
        print("Files OK.")
        time.sleep(1)

def init():
    try:
        print("Setting up farmbot...")
        checkFiles()
        
        # Gets the game's status, with the game's build
        gameStatus, gameBuild = getGameInfo()

        # Checks if the game is currently under maintenance
        if (gameStatus != "NORMAL"):
            print("Game is currently under maintenance, please wait until the maintainance is over!")
            input("Press enter to continue...")

        # Game's build version will always be == farmbot version
        if (not gameBuild == farmBotVersion):
            print("Farmbot is currently outdated, please wait for an update!")
            print(f"Game version: {gameBuild}\nFarmbot version: {farmBotVersion}")
            input("Press enter to continue...")


        startUpMenu()
    except:
        pass


if __name__ == "__main__":
    init()
