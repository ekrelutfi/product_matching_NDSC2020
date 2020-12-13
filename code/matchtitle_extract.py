import csv
from itertools import chain
##### read data, import, tokenisasi, remove punctuation ######
dummy = ['murah','termurah','promo','diskon','untuk','grosir','2020','1111','1212','gratis','berhadiah','']
with open('new_training_set.csv','r',encoding='UTF8') as file:
    test_sample = csv.reader(file, delimiter=',')
    data_sample=[]
    for row in test_sample:
        data_sample.append(row)
del data_sample[0]
for col in data_sample:
    del col[2]
    del col[3]

def convert(input, dummy="None"):
    import string
    punch = string.punctuation
    temp = [word.lower() for word in input.split()]
    words = []
    for word in temp:
        word = word.translate({ord(i): None for i in punch})
        words.append(word)
    while('' in words):
            words.remove('')
    if dummy!="None":
        for temp2 in dummy:
            if temp2 in words:
                words.remove(temp2)
    length = len(words)
    for x in range(length):
        if words[x].isdigit():
            if x==0:
                words[x] = words[x]+" "+words[x+1]
            elif x==length-1:
                words[x] = words[x-1]+" "+words[x]
            else:
                ins = words[x]+" "+words[x+1]
                words[x] = words[x-1]+" "+words[x]
                words.insert(x+1,ins)
    # words.sort()
    return(words)
###############
def checks(input1,input2):
    length1 = len(input1)
    length2 = len(input2)
    minlen = min(length1,length2)
    maxsim = 0
    for x in range(minlen):
        maxsim = maxsim+2*(x+1)
    sim = [[0 for i in range(length2)] for j in range(length1)]
    sumsim = 0
    for x in range(length1):
        for y in range(length2):
            if len(input1[x])<=len(input2[y]):
                if input1[x] in input2[y]:
                    sim[x][y]=1
                    sumsim=sumsim+1
                    # if x>0:
                    #     sim[x][y]=1+sim[x-1][y-1]
                    #     sumsim=sumsim+sim[x][y]+sim[x-1][y-1]
                    # else:
                    #     sim[x][y]=1
                    #     sumsim=sumsim+sim[x][y]
            else:
                if input2[y] in input1[x]:
                    sim[x][y]=1
                    sumsim=sumsim+1
                    # if x>0:
                    #     sim[x][y]=1+sim[x-1][y-1]
                    #     sumsim=sumsim+sim[x][y]+sim[x-1][y-1]
                    # else:
                    #     sim[x][y]=1
                    #     sumsim=sumsim+sim[x][y]
    if sumsim<minlen:
        match = sumsim/minlen
    else:
        match = 1
    return [match]
################################
def match(data, dummy="None"):
    nrow = len(data)
    data_match = [[0 for i in range(3)] for j in range(nrow)]
    for x in range(nrow):
        if dummy!="None":
            data_match[x][1] = convert(data[x][1],dummy)
            data_match[x][2] = convert(data[x][2],dummy)
        else:
            data_match[1] = convert(data[1])
            data_match[2] = convert(data[2])      
    match = [0 for i in range(len(data_match))]
    for i in range(len(data_match)):
        match[i] = checks(data_match[i][1],data_match[i][2])
    data=list(zip(data,match))
    return data
data= match(data_sample,dummy)
print(data[1])
with open('match_prod2.csv', mode='w') as csv_file:
    fieldnames = ['No', 'Title 1', 'Title 2','Match']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow({'No': row[0][0], 'Title 1': row[0][1], 'Title 2': row[0][2], 'Match': row[1][0]})
