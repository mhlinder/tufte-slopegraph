# http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0003nk

f = open('gnp.csv','r')
lines = f.readlines()
f.close()

head = lines[0].rstrip().split(',')
rows = [l.rstrip().split(',') for l in lines[1:]]
