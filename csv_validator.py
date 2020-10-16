import csv
import sys
import json
import re
import ntpath

# TODO: fix encoding errror in config file
# TODO: split file path to extract name

print("*"*50)
errors: dict = {}

if len(sys.argv) == 1:
    print("""
    Missing parameters !
    expected syntax : py app.py <csv_file> [<config_file>]
    """)
    sys.exit()

elif len(sys.argv) == 2:
    print("No config file given\nUsing default file './config.json'")
    csv_file = sys.argv[1]
    config_file = "./config.json"
else:
    csv_file = sys.argv[1]
    config_file = sys.argv[2]

print(f"csv file : {csv_file}")
print(f"config_file : {config_file}")


def logError(key, errorName, errorMessage=0):
    errors.setdefault(key, {}).setdefault(errorName, errorMessage)
    if type(errorMessage) == int:
        errors[key][errorName] += 1
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
        header = configs["cols"][index]["header"]
        for rule in rules:
            if not checkRule(cell, rule["regex"]):
                logError(header, rule["name"])
    pass


def checkHeaders(headers):
    for index, cell in enumerate(headers):
        header = configs["cols"][index]["header"]

        if header != cell:
            logError(header, 'Header',
                     f"expected: '{header}', actual: '{cell}'")
    pass


def checkFileName():
    filename = ntpath.basename(csv_file)

    for rule in configs["filename"]["rules"]:
        if not checkRule(filename, rule["regex"]):
            logError("filename", rule['name'])


def writeOutputFile():
    content = "TOUT EST OK - GO POUR DIFFUSION :D"
    with open('result.json', 'w') as json_file:
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
