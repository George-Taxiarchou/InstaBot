import csv

def scan(file):
    while True:
        field = next(file).split(",")
        field = [f.strip() for f in field]
        yield field

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def instaTarray(filename):
    file = open(filename,"r")
    teesgenerator = scan(file)
    teesfound = file_len(filename)
    tarray = []
    i=0
    while(i<teesfound):
        tee = next(teesgenerator)
        tarray.append([tee[0],int(tee[-2])])
        i+=1
    return tarray

def sortTees(array,i):
    tees = sorted(array, key=lambda score: score[i])
    return tees

def topTees(filename):
    LIKES = 1
    tarray = instaTarray(filename)
    print (len(tarray))
    tarray = sortTees(tarray,LIKES)
    for t in tarray:
        print (t)
    return tarray

def instalyticsCSV(tarray):
    instadir = open("instanalytics.csv","w")
    thoutput = csv.writer(instadir,delimiter = ',')
    for t in tarray:
        thoutput.writerow(t)

def instalyticA():
    instalyticsCSV(topTees("instarank.csv"))
