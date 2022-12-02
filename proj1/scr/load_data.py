
# read data from ../data/MSA_database.txt
def load_database():
    f = open("../data/MSA_database.txt", "r")
    file = f.readlines()
    # print(f.readlines())
    for i in range(len(file)):
        file[i] = file[i].strip("\n")
    return file
