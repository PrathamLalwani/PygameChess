import os

import scipy as sp
path = '/home/lalwani/Software_Projects/AIChess/images'
for filename in os.listdir(path):
    splitname = filename.split('_')
    if len(splitname)>1:
        if splitname[1] == 'king':
            newname = splitname[0] + 'c.png'
        else:
            newname = splitname[0] + splitname[1][0] + '.png'
        os.rename(os.path.join(path,filename), os.path.join(path,newname))
    