import srcomapi, srcomapi.datatypes as dt
import datetime
from easygui import *
api = srcomapi.SpeedrunCom()

base = True

def baseMenu():
    choice = indexbox("Select a category", "Menu", ["100%", "Bosses", "Chapters", "Other"])

    if choice == None:
        quit()
    elif choice == 0:
        find100()
    elif choice == 1:
        findBoss()
    elif choice == 2:
        findLevels()
    elif choice == 3:
        findOther()

def extMenu():
    choice = indexbox("Select a category", "Menu", ["Death%", "I am frustrated.", "Levels", "Other"])

    if choice == None:
        quit()
    elif choice == 0:
        findDeath()
    elif choice == 1:
        findFrus()
    elif choice == 2:
        findExLevels()
    elif choice == 3:
        findOtherExten()

def runLoop(string, values=[1,1], mult=False):
    priStr = "Run(s): \n \n"
    ldboard = dt.Leaderboard(api, data=api.get(string))
    for i in range(int(values[0])-1, int(values[1])):
        currentRun = ldboard.runs[i]["run"]
        if mult == False:
            priStr += str(i+1) + ". " + str(datetime.timedelta(seconds=currentRun.times["primary_t"]))[:-3] + " by " + str(currentRun.players[0].name) +  "\n"
        else:
            players = ""
            for player in currentRun.players:
                players += str(player.name) + " and "
            priStr += str(i+1) + ". " + str(datetime.timedelta(seconds=currentRun.times["primary_t"]))[:-3] + " by " + players[:-5] +  "\n"
    msgbox(priStr)
    if base:
        baseMenu()
    else:
        extMenu()

def get_values():
    values = []
    userInput = enterbox("Input the run(s) to find: ")
    if "-" in userInput:
        values = userInput.split("-")
        if len(values) != 2:
            msgbox("An invalid number of runs was entered, defaulting to WR")
            values = [1, 1]
    else:
        try: 
            userInput = int(userInput)
            values = [userInput, userInput]
        except ValueError:
            msgbox("A number was not entered, defaulting to WR")
            values = [1, 1]

    return values

def findOther():
    cateInput = indexbox("What category?", choices=["Any% NMG", "Any%", "Alt Ending", "All Collectibles", "No Shortcuts"])
    if cateInput == None:
        baseMenu()
    elif cateInput == 4:
        cateInput = 10
    cate = cates[cateInput]
    difficultyVar = cate.variables[0]
    diffList = ["IE", "EE", "VE", "Easy"]

    diffInput = enterbox("Input the runs difficulty: ")
    for x in diffList:
        if diffInput.lower() == x.lower():
            diff = diffList.index(x)
            break
    else:
        msgbox("An invalid difficulty was entered, defaulting to Infinitely Easy")
        diff = 0

    cateString = "leaderboards/{}/category/{}?var-{}={}".format(wys.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[diff])
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base: baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

def findLevels():
    diffList = ["IE", "EE", "VE", "Easy"]
    diffInput = enterbox("Input the difficulty: ")
    for x in diffList:
        if diffInput.lower() == x.lower():
            diff = diffList.index(x)
            break
    else:
        msgbox("Difficulty could not be found, defaulting to Infinitely Easy")
        diff = 0

    difficultyVar = cates[diff+4]
    aop = difficultyVar.variables[0]

    levelInput = enterbox("Input the chapter name: ")
    for x in levels:
        if levelInput.lower() == x.name.lower():
            level = x
            break
    else:
        msgbox("Chapter could not be found, defaulting to Chapter A")
        level = levels[0]

    aopInput = indexbox("Choose the category?", choices=["Any%", "All Puzzles"])
    if aopInput == None:
        baseMenu()

    cateString = "leaderboards/{}/level/{}/{}?var-{}={}".format(wys.id, level.id, difficultyVar.id, aop.id, list(aop.data["values"]["choices"].keys())[aopInput])
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base:
            baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])


def findExLevels():

    diffInput = indexbox("Select the runs category", choices=["Any%", "Pump Broken", "Exploration Point"])
    if diffInput == None:
        baseMenu()
    else:
        diff = diffInput
    
    difficultyVar = cates[diff+6]

    levelInput = enterbox("Input the level: ")
    for x in levels:
        if levelInput.lower() == x.name.lower():
            level = x
            break
    else:
        msgbox("Level could not be found, defaulting to A01")
        level = levels[0]

    cateString = "leaderboards/{}/level/{}/{}".format(wys.id, level.id, difficultyVar.id)
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base:
            baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

def find100():
    cate = cates[8]
    cateString = "leaderboards/{}/category/{}".format(wys.id, cate.id)
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base:
            baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

def findBoss():
    cate = cates[9]
    difficultyVar = cate.variables[0]
    bossVar = cate.variables[1]
    diffList = ["IE", "EE", "VE", "Easy"]
    bossList = ["Splitty", "Mr D.A.N.C.E", "Mama Squid", "Helpy", "Bartender", "Squid 1", "Squid 2"]

    diffInput = enterbox("Input the boss difficulty: ")
    for x in diffList:
        if diffInput.lower() == x.lower():
            diff = diffList.index(x)
            break
    else:
        msgbox("An invalid difficulty was entered, defaulting to Infinitely Easy")
        diff = 0

    bossInput = enterbox("Input the boss: ")
    for x in bossList:
        if bossInput.lower() == x.lower():
            boss = bossList.index(x)
            break
    else:
        msgbox("An invalid boss was entered, defaulting to Splitty")
        boss = 0

    cateString = "leaderboards/{}/category/{}?var-{}={}&var-{}={}".format(wys.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[diff], bossVar.id, list(bossVar.data["values"]["choices"].keys())[boss])
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base: baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

def findOtherExten():

    cateInput = indexbox("What category?", choices=["Chapter Relay", "Double-Time", "Block Massacre", "Minimum Kills"])
    if cateInput == None:
        extMenu()
    elif cateInput == 1:
        cateInput = 2
    elif cateInput == 2:
        cateInput = 4
    elif cateInput == 3:
        cateInput = 5
    cate = cates[cateInput]

    difficultyVar = cate.variables[0]
    diffList = ["IE", "EE", "VE", "Easy"]

    diffInput = enterbox("Input the runs difficulty: ")
    for x in diffList:
        if diffInput.lower() == x.lower():
            diff = diffList.index(x)
            break
    else:
        msgbox("An invalid difficulty was entered, defaulting to Infinitely Easy")
        diff = 0

    cateString = "leaderboards/{}/category/{}?var-{}={}".format(wys.id, cate.id, difficultyVar.id, list(difficultyVar.data["values"]["choices"].keys())[diff])
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values, True)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base: baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1], True)

def findDeath():
    cate = cates[3]
    cateString = "leaderboards/{}/category/{}".format(wys.id, cate.id)
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base: baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

def findFrus():
    cate = cates[1]
    levelVar = cate.variables[0]
    levelInput = indexbox("Select which level", choices=["2", "25", "50", "75", "100", "1000"])
    if levelInput == None:
        extMenu()

    cateString = "leaderboards/{}/category/{}?var-{}={}".format(wys.id, cate.id, levelVar.id, list(levelVar.data["values"]["choices"].keys())[levelInput])
    values = get_values()

    try:
        dt.Leaderboard(api, data=api.get(cateString)).runs[int(values[-1])-1]
        runLoop(cateString, values)
    except IndexError:
        msgbox("There is no run number " + str(values[-1]) + ", please enter a valid run")
        if base: baseMenu()
        else: extMenu()
    except ValueError:
        msgbox("A number was not entered for a value, defaulting to WR")
        runLoop(cateString, [1,1])

main = indexbox("Select which leaderboard", "Main Menu", ["Full Game + Chapters", "Category Extensions + Levels"])
if main == None:
    quit()
if main == 0:
    wys = api.search(srcomapi.datatypes.Game, {"name": "will you snail?"})[0]
    cates = wys.categories
    levels = wys.levels
    baseMenu()

elif main == 1:
    wys = api.search(srcomapi.datatypes.Game, {"name": "will you snail?"})[3]
    cates = wys.categories
    levels = wys.levels
    base = False
    extMenu()