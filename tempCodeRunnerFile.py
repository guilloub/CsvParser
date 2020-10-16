with open(csv_file, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        checkRow(row)
