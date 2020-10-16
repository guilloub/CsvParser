import csv
import sys
import json
import re

print("*"*50)

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
    for col_index, cell in enumerate(row):
        print(col_index, cell)
    pass


def checkHeaders(headers):
    for col_index, cell in enumerate(headers):
        print(col_index, cell)
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


# checkFileName()

with open(csv_file, newline='') as f:
    reader = csv.reader(f, delimiter=';')

    for row_index, row in enumerate(reader):
        if(row_index == 0):
            checkHeaders(row)
            print('-'*50)
        elif(row_index < 3):
            checkRow(row)
        else:
            break
