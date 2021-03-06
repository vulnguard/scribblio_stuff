import random
import pprint
import sys


pp = pprint.PrettyPrinter(indent=4)

DEFAULT_IN = "wordlist.txt"
DEFAULT_OUT = "output.txt"


def get_filenames_from_args():
    # Default Filenames
    infile, outfile = DEFAULT_IN, DEFAULT_OUT
    
    if len(sys.argv) >= 3:
        infile = sys.argv[2]

    if len(sys.argv) >= 4:
        outfile = sys.argv[3]

    return infile, outfile

def main():
    print("=" * 9 + " START " + "=" * 9)

    if len(sys.argv) > 1:
        # DIFF
        if sys.argv[1] == "--diff":
            infile, outfile = get_filenames_from_args()
            diff(infile, outfile)

        # CHECK
        elif sys.argv[1] == "--check":
            infile, outfile = get_filenames_from_args()
            check(infile, outfile)

        # CATEGORISE
        elif sys.argv[1] == "--categorise":
            infile, outfile = get_filenames_from_args()
            manual_categorise(infile, outfile)

        elif sys.argv[1] == "--to_txt":
            infile, outfile = sys.argv[2], sys.argv[3]
            to_csv_txt(infile, outfile)

        # RANDOMISE
        elif sys.argv[1] == "--random":
            infile, outfile = get_filenames_from_args()

            randomise(infile, outfile)

        # Unknown args
        else:
            print("unknown args")
            print_usage()

    # Unknown args
    else:
        print("unknown args outside")
        print_usage()

    print("=" * 9 + " END " + "=" * 9)


def manual_categorise(infile, outfile):
    if not outfile.endswith(".categorised.txt"):
        if outfile.endswith(".txt"):
            outfile = outfile[:-4] + ".categorised.txt"

    words, categorised = get_words(infile) 

    cat_words = []

    categories = []
    if categorised:
        for word in words:
            if not word[1] in categories:
                categories.append(word[1])

    count = 0

    prev_category = "UNCATEGORISED"

    while count < len(words):
        pair = words[count]

        if categorised:
            word = pair[0]
            category = pair[1]

        if categorised:
            print("=== " + word + ": " + category + " === {}/{}".format(count + 1, len(words)))
        else:
            print("=== " + word + ": " + "UNCATEGORISED ===" + " {}/{}".format(count + 1, len(words)))

        print("Available categories:")
        for ii in range(0, len(categories) - 1):
            print(categories[ii], end=", ")
        if len(categories) != 0:
            print(categories[-1])

        choice = input()

        # Used later for if we are jsut changing to a different index in the list.
        try:
            i = int(choice)
            isint = True
        except Exception as e:
            isint = False

        # Use last category
        if choice == '':    

            if categorised:
                if category == "UNCATEGORISED":
                    print("Using previous category: " + prev_category + "\n")
                    cat_words.append([word, prev_category])

                else:
                    print("Unchanged.")
                    cat_words.append([word, category])
            else:
                print("Using previous category: " + prev_category + "\n")
                cat_words.append([word, prev_category])

            count += 1

        # Go to index
        elif isint:
            new_index = int(choice) - 1
            if new_index > len(words):
                new_index = len(words) - 1

            while count < new_index:
                if categorised:
                    cat_words.append([word, category])
                else:
                    cat_words.append([word, "UNCATEGORISED"])
    
                count += 1
                word = words[count]
                if categorised:
                    word = word[0]
                    category = word[1]

        # Delete
        elif choice == 'd':
            print("Delete '{}', are you sure? (y/n)".format(word))
            delete = input()
            if delete == "y":
                # Dont add the word to the new list
                print("Deleted '{}'".format(word))
            else:
                print("No change")
                cat_words.append([word, category])

            count += 1

        # Go back
        elif choice == 'b':
            count -= 1
            del cat_words[-1]

        # Modification
        else:
            print("Adding category '{}' to '{}'\n".format(choice, word))

            prev_category = choice
            if choice not in categories:
                categories.append(choice)

            cat_words.append([word, choice])
            count += 1


    write_categorised_words(cat_words, outfile)




def print_usage():
    print("Usage:")
    print("python script.py FUNCTION")
    print("Available functions:")
    print("--diff [file1] [file2]")
    print("--check [infile] [outfile]")
    print("--categorise [infile] [outfile]")
    print("--to_txt infile outfile")
    print("--random [infile] [outfile]")


def get_good_input(valid_inputs = [], isint=False, prompt = "", int_range = ["min", "max"]):
    coice = ""

    if int_range[0] == "min":
        int_range[0] = -999999

    if int_range[1] == "max":
        int_range[1] = 999999


    if len(valid_inputs) == 0 and not isint:
        raise Exception("No valid inputs given")

    choice = "TEMP"

    if isint:
        valid = False
        while not valid:
            try:
                choice = int(input())
                if choice >= int_range[0] and choice <= int_range[1]:
                    valid = True

                else:
                    valid = True
            except Exception as e:
                #print(e)
                #print(choice)
                #print("{}, {}".format(int_range[0], int_range[1]))
                print("Please enter an integer")

    else:
        while choice not in valid_inputs:
            if not prompt == "":
                print(prompt)
            choice = input()

    return choice


def randomise(infile, outfile):
    words, categorised = get_words(infile)

    possible_words = []
    random_words = []

    print("Num words: ")
    num_words = get_good_input(isint=True, int_range = [1, "max"])

    print("Minimum word length: ")
    min_word_len = get_good_input(isint=True, int_range = [1, "max"])

    print("Maximum word length: ")
    max_word_len = get_good_input(isint=True, int_range = [1, "max"])

    avail_words = words

    if not categorised:
        print("Un-categorised words given.")

    else:
        categories = []
        all_categories = []

        for word in words:
            if word[1] not in categories:
               categories.append(word[1])
               all_categories.append(word[1])


        choice = "BLAH"
    
        allowed_returns = []

        while not choice == "":
            print("Available categories:")
            pp.pprint(categories)
            print("Enter categories to NOT to include, enter nothing to continue. Enter '-CategoryName' to re-add.")
    
            choice = get_good_input(valid_inputs = categories + [""] + allowed_returns)
    
            if not choice == "":
                if choice[0] == "-":
                    if choice[1:] in all_categories:
                        categories.append(choice[1:])
                    else:
                        print("Unknown category '{}'".format(choice))
                else:
                    categories.remove(choice)
                    allowed_returns.append("-" + choice)

        print("Remaining categories:")
        print(categories)

        # Check word categories and add to avail words
        avail_words = []
        for word in words:
            if word[1] in categories:
                avail_words.append(word[0])


    # Laziness
    words = avail_words


    # Check word lengths
    index = 0
    while index < len(words):
        word = words[index]
        if len(word) <= max_word_len and len(word) >= min_word_len:
            possible_words.append(word)

        index += 1

    # Check if we have enough words, print warning if we dont.
    if len(possible_words) <= num_words:
        print("Only {} words match length criteria, using all of them.".format(len(possible_words)))
        random_words = possible_words

    # Select random ones based on num_words
    else:
        while len(random_words) < num_words:
            chosen_word = possible_words[random.randint(0, len(possible_words) - 1)]

            if not chosen_word in random_words:
                random_words.append(chosen_word)

    print("Random words. number={}, min_Len={}, max_len={}".format(num_words, min_word_len, max_word_len))
    pp.pprint(random_words)

    write_words(random_words, outfile)


def check(infile, outfile):
        word_list = get_words(infile)

        checked_words = manual_check_words(word_list)

        # Remove duplicates
        checked_words = dedup(checked_words)

        # pp.pprint(checked_words)
        write_words(checked_words, outfile)

def write_words(words, outfile):
        with open(outfile, "w") as f:
            string = ""
            for word in words:
                string += word + ","
        
            string = string[:-1]
        
            f.write(string)


def write_categorised_words(words, outfile):
    if not outfile.endswith(".categorised.txt"):
        outfile = outfile.rstrip(".txt")
        outfile += ".categorised.txt"

    with open(outfile, "w") as f:
        string = ""
        for word in words:
            string += (word[0] + ": " + word[1] + "\n")

        string = string[:-1]

        f.write(string)


def dedup(words):
    count = 0
    while count < len(words):
        word = words[count].lower()

        check_count = count + 1
        while check_count < len(words):
            check_word = words[check_count].lower()
            if check_word == word:
                print("Duplicate: {}".format(word))
                del words[check_count]

            check_count += 1

        count += 1

    return words

def manual_check_words(words):
    checked_words = []

    count = 0

    while count < len(words):
        word = words[count]

        print(word + " {}/{}".format(count + 1, len(words)))

        choice = input()

        try:
            i = int(choice)
            isint = True
        except Exception as e:
            isint = False

        # Do nothing
        if choice == '':
            print("No change")
            checked_words.append(word)

            count += 1

        elif isint:
            new_index = int(choice) - 1
            if new_index >= len(words):
                new_index = len(words) - 1

            while count < new_index:
                checked_words.append(word)
                count += 1
                word = words[count]

        # Delete
        elif choice == 'd':
            print("Delete '{}', are you sure? (y/n)".format(word))
            delete = input()
            if delete == "y":
                # Dont add the word to the new list
                print("Deleted '{}'".format(word))
            else:
                print("No change")
                checked_words.append(word)

            count += 1

        # Go back
        elif choice == 'b':
            count -= 1
            del checked_words[-1]

        # Modification
        else:
            print("Changing '{}' to '{}'\n".format(word, choice))
            checked_words.append(choice)
            count += 1


    return checked_words


def diff(file1, file2):
    words1_orig = get_words(file1)
    words2_orig = get_words(file2)
        
    words1_lower = [word.lower() for word in words1_orig]
    words2_lower = [word.lower() for word in words2_orig]

    print("f1 {} vs f2 {}".format(len(words1_orig), len(words2_orig)))

    print("-" * 3 + "in {} but not {}".format(file1, file2) + "-" * 3)

    for word in words1_orig:
        if not word.lower() in words2_lower:
            print(word)
            
    print("-" * 3 + "in {} but not {}".format(file2, file1) + "-" * 3)

    for word in words2_orig:
        if not word.lower() in words1_lower:
            print(word)


def get_words(filename):
    if filename.endswith(".categorised.txt"):
        print("Loading categorised data from '{}'.".format(filename))
        return get_categorised_words(filename), True
    else:
        print("Loading un-categorised data from '{}'.".format(filename))
        return get_uncategorised_words(filename), False


def get_categorised_words(filename):
    if not filename.endswith(".categorised.txt"):
        print("=== WARNING === Filename does not end with .categorised.txt")

    try:
        words = open(filename, "r").read().split("\n")
    except FileNotFoundError as e:
        print("File '{}' not found.".format(filename))
        exit(-1)

    categorised_words = []

    for pair in words:
        word, category = pair.split(": ")

        word = word.lstrip().lstrip("\n")
        word = word.rstrip().rstrip("\n")

        category = category.lstrip().lstrip("\n")
        category = category.rstrip().rstrip("\n")

        categorised_words.append([word, category])

    return categorised_words


def to_uncat_words(cat_words):
    uncat_words = []

    for word in cat_words:
        uncat_words.append(cat_words[0])

    return uncat_words

def to_csv_txt(infile, outfile):
    if not infile.endswith(".categorised.txt"):
        return

    print("Converting file to plain CSV. WARNING: Removes categories.")

    words = get_categorised_words(infile)
    
    wordstr = ""
    for word in words:
        wordstr += word[0] + ","
    
    wordstr = wordstr[:-1]

    if outfile.endswith(".categorised.txt"):
        print("=== WARNING === Stripping categorised.txt from outfile name")
        outfile.rstrip(".categorised.txt")

    open(outfile, "w").write(wordstr)


def get_uncategorised_words(filename):
    try:
        words = open(filename, "r").read().split(",")
    except FileNotFoundError as e:
        print("File '{}' not found.".format(filename))
        exit(-1)

    good_words = []

    for word in words:
        new_word = word.lstrip().lstrip("\n")
        new_word = new_word.rstrip().rstrip("\n")

        if len(new_word) != 0:
            good_words.append(new_word.lstrip())

    return good_words

if __name__ == "__main__":
    main()
