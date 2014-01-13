# http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0003nk

def json_csv(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    head = lines[0].rstrip().split(',')
    rows = [l.rstrip().split(',') for l in lines[1:]]

    json = {}
    for row in rows:
        country = row[0]
        row = [float(row[1]), float(row[2])]
        json[country] = dict(zip(head[1:],row))
    return json

filename = "gnp.csv"
title = "Current Receipts of Government as a Percentage of Gross Domestic Product, 1970 and 1979"
data = json_csv(filename)
