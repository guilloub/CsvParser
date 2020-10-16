import csv
import sys
import json
import re


print("*"*50)
errors: dict = {}

if len(sys.argv) == 1:
    print("""
    Missing parameters !
    expected syntax : py app.py <csv_file> [<config_file>]
    """)
    # sys.exit()
    csv_file = "d:\projets\HelloPython\samples\\alertes2020012207.csv"
    config_file = "./config.json"

elif len(sys.argv) == 2:
    print("No config file given\nUsing default file './config.json'")
    csv_file = sys.argv[1]
    config_file = "./config.json"
else:
    csv_file = sys.argv[1]
    config_file = sys.argv[2]

print(f"csv file : {csv_file}")
print(f"config_file : {config_file}")


with open(config_file) as f:
    configs = json.load(f)


###
#  Verify if the value string is an exact match for the regex
###
def checkRule(value: str, regex: str) -> bool:
    p = re.compile(regex)
    m = p.fullmatch(value)
    if m:
        return True
    else:
        return False


def checkRow(row):
    for index, cell in enumerate(row):
        rules = configs["cols"][index]["rules"]
        for rule in rules:
            if not checkRule(cell, rule["regex"]):
                logError(index, rule["name"])
    pass


def logError(col_index, errorName, errorMessage=0):
    col_index += 1
    errors.setdefault(col_index, {}).setdefault(errorName, errorMessage)
    if type(errorMessage) == int:
        errors[col_index][errorName] += 1
    pass


def checkHeaders(headers):
    for index, cell in enumerate(headers):
        title = configs["cols"][index]["title"]

        if title != cell:
            logError(index, 'Title', f"expected: '{title}', actual: '{cell}'")
    pass


def checkFileName():
    print("filename: ", csv_file)

    has_errors = False
    for rule in configs["filename"]["rules"]:
        if not checkRule(csv_file, rule["regex"]):
            print(f"Rule '{rule['name']}' not respected")
            has_errors = True
        else:
            print(f"rule '{rule['name']}' OK")

    if not has_errors:
        print("All rules OK")


def writeOutputFile():
    content = "TOUT EST OK - GO POUR DIFFUSION :D"
    with open('result.json', 'w') as json_file:
        if len(errors) != 0:
            content = errors
        print(errors)
        json.dump(content, json_file, indent=2, sort_keys=True)


with open(csv_file, newline='') as f:
    reader = csv.reader(f, delimiter=';')

    for row_index, row in enumerate(reader):
        if(row_index == 0):
            checkHeaders(row)
        # elif(row_index <= 100):
        #     checkRow(row)
        else:
            checkRow(row)
    writeOutputFile()        # break
