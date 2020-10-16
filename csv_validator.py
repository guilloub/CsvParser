import csv
import sys
import json
import re

# TODO: fix encoding errror in config file
# TODO: split file path to extract name

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


def logError(col_index, errorName, errorMessage=0):
    if isinstance(col_index, int):
        col_index += 1
    errors.setdefault(col_index, {}).setdefault(errorName, errorMessage)
    if type(errorMessage) == int:
        errors[col_index][errorName] += 1
    pass

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


def checkHeaders(headers):
    for index, cell in enumerate(headers):
        header = configs["cols"][index]["header"]

        if header != cell:
            logError(index, 'Header',
                     f"expected: '{header}', actual: '{cell}'")
    pass


def checkFileName():
    has_errors = False
    for rule in configs["filename"]["rules"]:
        if not checkRule(csv_file, rule["regex"]):
            logError("filename", rule['name'])


def writeOutputFile():
    content = "TOUT EST OK - GO POUR DIFFUSION :D"
    with open('result.json', 'w', encoding='utf-8') as json_file:
        if len(errors) != 0:
            content = errors
            print("DES ERREURS ONT ETE DETECTEES :(")
        else:
            print(content)
        json.dump(content, json_file, indent=2)


with open(config_file, encoding='utf-8') as f:
    configs = json.load(f)

checkFileName()

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
