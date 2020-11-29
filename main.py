from termcolor import cprint
import numpy as np
from tabulate import tabulate
from mongo_class import Mongo_db
import random


def Test_1(responds, df):
    total = np.sum([responds[i] == df[i]['Person'] for i in range(len(responds))]) / len(responds)
    data = {"Total": total}
    total_data = {}
    for i in persons:
        data[i] = None
        total_data[i] = 0

    for i in range(len(responds)):
        if responds[i] == df[i]['Person']:
            if data[df[i]['Person']] == None:
                data[df[i]['Person']] = 1
            else:
                data[df[i]['Person']] += 1
        total_data[df[i]['Person']] += 1

    for i in data:
        if data[i] is not None and i != "Total":
            data[i] = data[i] / total_data[i]
        elif data[i] is None:
            data[i] = "None"

    return data.items()

def Test_1a(responds, df):
    data = {}
    total_data = {}
    for i in persons:
        data[i] = {}
        total_data[i] = 0
        for j in persons:
            data[i][j] = 0
    for i in range(len(responds)):
        aux = df[i]['Person']
        data[aux][responds[i]] += 1
        total_data[aux] += 1
    data2 = {}
    for i in data:
        for j in persons:
            if total_data[i] > 0:
                data2[i + "-" + j] = data[i][j] / total_data[i]
    return data2.items()



def Test_2(responds):
    data = {}
    for i in persons:
        data[i] = []
    for r in responds:
        data[r[1]].append(r[0])
    for d in data:
        if data[d] == []:
            data[d] = "None"
        else:
            data[d] = np.mean(data[d])
    return data.items()

### LOADING DATA
try:
    user = input("User: ")
    pwd = input("Pasword: ")
    db = Mongo_db(user, pwd)
    persons, short = db.get_persons()
    responds_ = db.get_sentences()
    df = db.get_Text()
except:
    cprint("Wrong user or password :(", 'red')
    exit()

random.shuffle(df) # Shuffle sentences
df = df[:30] # Set number tests

### PRINT INSTRUCTIONS
logo = open("logo.txt", "r")
print(logo.read())
for p, s in zip(persons, short):
    print("    - " + p + " (" + s + ")")
print('')
print('########################################################################################################################')

cprint("Are you ready?", 'blue')
_ = input("Type answer: ")

try:
    ### TEST 1
    cprint("First Test: Who is this person?", 'blue')
    responds = []
    for i in range(len(df)):
        cprint("Question " + str(i + 1), 'blue')
        cprint("Sentences:", 'green')
        print('########################################################################################################################')
        print(df[i]['Sentences'])
        print('########################################################################################################################')
        while True:
            cprint("Who you think is:", 'green')
            for p, s in zip(persons, short):
                print("    - " + p + " (" + s + ")")
            aux = input("Type answer: ")
            if aux in persons or aux in short:
                if aux in short:
                    aux = persons[short.index(aux)]
                responds.append(aux)
                a = np.random.choice(len(responds_))
                cprint(responds_[a], 'cyan')
                break
            if aux == "Who?":
                d = open("config.txt", "r")
                cprint(d.read(), 'blue')
            cprint("You have to type one of the options", "yellow")
        print('########################################################################################################################')

    """
    ### TEST 2
    cprint("Second Test: How good I did it?", 'blue')
    responds2 = []
    for i in range(len(df)):
        cprint("Question " + str(i + 1), 'blue')
        cprint("Author:", 'green')
        print("    "  +  df[i]['Person'])
        cprint("Sentences:", 'green')
        print('########################################################################################################################')
        print(df[i]['Sentences'])
        print('########################################################################################################################')
        while True:
            cprint("How I did it? [0-10]", 'green')
            print(" 0: Horrible")
            print(" ...........")
            print(" 10: Perfect")
            while True:
                try:
                    aux = int(input("Type answer: "))
                    break
                except ValueError:
                    cprint("Must be a Integer", )
            if 0 <= aux <= 10:
                responds2.append([aux, df[i]['Person']])
                a = np.random.choice(len(responds_))
                cprint(responds_[a], 'cyan')
                break
            if aux == "Who?":
                d = open("config.txt", "r")
                cprint(d.read(), 'blue')
            cprint("You have to put a number between 0 - 10", "yellow")
        print('########################################################################################################################')
    """
    ### PLOT RESULTS
    cprint("Results from Test 1", 'blue')
    test_1 = Test_1(responds, df)
    print(tabulate(test_1, ["Type", "Porcentage [0-1]"], tablefmt="fancy_grid"))
    test_1a = Test_1a(responds, df)
    print(tabulate(test_1a, ["Type", "Porcentage [0-1]"], tablefmt="fancy_grid"))
    test_1 = dict(test_1)
    test_1.update(test_1a)
    db.insert_Test_1(test_1)

    #cprint("Results from Test 2", 'blue')
    #test_2 = Test_2(responds2)
    #print(tabulate(test_2, ["Person", "Average"], tablefmt="fancy_grid"))
    #db.insert_Test_2(test_2)

    cprint("Thanks for participate :D", 'blue')
except KeyboardInterrupt:
    cprint("\nGuess we can do it later :D", 'blue')


