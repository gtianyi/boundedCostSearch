import fileinput

for line in fileinput.input(inplace=True):
    if line[-2] == '}':
        print(line[:-1])
    elif line[-3] == '}':
        print(line[:-2])
    elif line[-4] == '}':
        print(line[:-3])
    else:
        print(line)
