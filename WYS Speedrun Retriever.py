import srcomapi, srcomapi.datatypes as dt
import datetime
from easygui import *
api = srcomapi.SpeedrunCom()
wys = api.search(srcomapi.datatypes.Game, {"name": "will you snail?"})[0]
cates = wys.categories

def runLoop(string, values=[1,1]):
    priStr = "Run(s): \n \n"
    ldboard = dt.Leaderboard(api, data=api.get(string))
    for i in range(int(values[0])-1, int(values[1])):
        currentRun = ldboard.runs[i]["run"]
        priStr += str(datetime.timedelta(seconds=currentRun.times["primary_t"]))[:-3] + " by " + str(currentRun.players[0].name) +  "\n"
    msgbox(priStr)
    menu()

def findOther():
    cateInput = indexbox("What category?", choices=["Any% NMG", "Any%", "Alt Ending", "All Collectibles", "No Shortcuts"])
    if cateInput == None:
        menu()
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
    except ValueError:
        msgbox("A number was not entered for a value")


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
            values = [1, userInput]
        except ValueError:
            msgbox("A number was not entered, defaulting to WR")
            values = [1, 1]

    return values

def menu():
    choice = indexbox("Select an option", "Menu", ["100%", "Bosses", "Other"])

    if choice == None:
        quit()
    elif choice == 0:
        find100()
    elif choice == 1:
        findBoss()
    elif choice == 2:
        findOther()

menu()   