#!/usr/bin/env python

import random

def get_p(fi):
    lis =list(fi)
    number = []
    number.append(int(lis[0]) * 1000 + int(lis[1]) * 100 + int(lis[2]) * 10 + int(lis[3]))
    number.append(int(lis[5]) * 1000 + int(lis[6]) * 100 + int(lis[7]) * 10 + int(lis[8]))
    number.append(int(lis[10]) * 1000 + int(lis[11]) * 100 + int(lis[12]) * 10 + int(lis[13]))
    return number

def write_file(fi, num):
    with open(fi, 'w') as fo:
        spc = ' '
        endl = '\n' 
        str_num = [str(int) for int in num]
        fo.write(spc.join(str_num) + endl)
        randomScore = []
        for i in range(0, num[0]):
            randomScore.append(str(random.randint(1, 999)))
        fo.write( spc.join(randomScore) + endl)
        for i in range(0, num[1]):
            if (num[0] < 20):
                nbooks = random.randint(1, num[0])
            else:
                nbooks = random.randint(1, 20)
            fo.write(str(nbooks) +spc+ str(random.randint(1,10)) +spc+ str(random.randint(1, 5)) + endl)
            randomBooks = random.sample(range(num[0]), nbooks)
            fo.write(spc.join(str(x) for x in randomBooks) + endl)


if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    num = get_p(file_name)
    write_file(file_name, num)

