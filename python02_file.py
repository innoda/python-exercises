# task 1.0 - init
import csv

FILENAME = "names.csv"
FILE_START_YEAR = 1895
START_YEAR = 1950
END_YEAR = 2013

def read_lines():
    with open(FILENAME, newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        lines = []
        for line in reader:
            if line != "":
                lines.append(line)
                
    lines = retype_lines(lines)
    return lines

def retype_lines(lines):
    for i in range (len(lines)):
        for j in range (1, len(lines[i])):
            lines[i][j] = int(lines[i][j])
    return lines

def make_name_dictionary(lines):
    names = {}
    for i in range (1, len(lines)):
        names[lines[i][0]] = lines[i][START_YEAR - FILE_START_YEAR:END_YEAR - FILE_START_YEAR+1]
    return names

NAME_DICTIONARY = make_name_dictionary(read_lines())


# task 1.1
def top_names(since, to, top_n, reversed=False):
    if not check_date_input(since, to):
        return

    if not check_topn(top_n):
        return
        
    names = NAME_DICTIONARY
    since, to = recount_years(since, to)
    
    names_count = count_names_occurence(names, since, to, top_n)

    if reversed:
        for key in sorted(names_count, key=lambda x: names_count[x])[:top_n]:
            print("name: " + str(key) + ", count: " + str(names_count[key]))
    else:
        for key in sorted(names_count, key=lambda x: -names_count[x])[:top_n]:
            print("name: " + str(key) + ", count: " + str(names_count[key]))

def count_names_occurence(names, since, to, top_n):
    names_count = {}
    for name in names:
        array = names[name]
        sum = 0
        for j in range (since, to):
            sum += array[j]
        names_count[name] = sum
    return names_count


# task 1.2
def popularity(since, to, name):
    if not check_date_input(since, to):
        return

    names = NAME_DICTIONARY
    name = name.upper()
    if not check_name(names, name):
        return
    
    since, to = recount_years(since, to)
  
    array = names[name]
    current = 0
    for i in range (since, to):
        print(i+START_YEAR, array[i] - current)
        current = array[i]


# task 1.3
def top_for_years(since, to):
    if not check_date_input(since, to):
        return
    
    for i in range(since, to+1):
        print(str(i) + " top: ", end="")
        top_names(i, i, 1, False)
        print(str(i) + " drop: ", end="")
        top_names(i, i, 1, True)
        print()


# task 1.4
def first_letter_analysis(since, to, letter):
    if not check_date_input(since, to):
        return
    
    letter = letter.upper()
    if not check_letter(letter):
        return
    
    names = NAME_DICTIONARY
    since, to = recount_years(since, to)
        
    candidates = dict((key,value) for key, value in names.items() if key[0] == letter)

    i = since
    while (i < to):
        names_for_year = count_names_occurence(candidates, i, i+1, 1)
        sorted_names = sorted(names_for_year, key=lambda x: -names_for_year[x])
    
        key = sorted_names[0]
        print("top name of the year " + str(i+START_YEAR) + ": " + key + ", count: " + str(names_for_year[key]))

        for j in range(1, len(sorted_names)):
            key = sorted_names[j]
            if names_for_year[key] == 0:
                break
            print("name: " + str(key) + ", count: " + str(names_for_year[key]))
        print()
        i += 1
        print(i, since, to)

def recount_years(since, to):
    return (since-START_YEAR, to-START_YEAR+1)

def check_date_input(since, to):
    result = True
    if since < START_YEAR:
        print("Start date must be " + str(START_YEAR) + " at least.")
        result = False
    if to < START_YEAR:
        print("End date must be " + str(START_YEAR) + " at least.")
        result = False
    if since > END_YEAR:
        print("Start date must be " + str(END_YEAR) + " at most.")
        result = False
    if to > END_YEAR:
        print("End date must be " + str(END_YEAR) + " at most.")
        result = False
    if to < since:
        print("End date must be greater than start date.")
        result = False
    return result

def check_topn(top_n):
    if top_n < 1:
        print("No value will be displayed: top_n is less than 1.")
        return False
    return True

def check_name(names, name):
    if not name in names:
        print("Given name " + name + " is not in names dictionary.")
        return False
    return True

SPECIAL_LETTERS = ["Á", "É", "Í", "Ó", "Ú", "Ý", "Č", "Ď", "Ň", "Ř", "Š", "Ť", "Ž"]
    
def check_letter(letter):
    if ord(letter) < 65 or ord(letter) > 90 and letter not in SPECIAL_LETTERS:
        print("Invalid starting letter.")
        return False
    return True
    
