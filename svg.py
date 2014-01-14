from svgwrite import Drawing
from pandas import read_csv
from numpy import min, max, arange, argsort

# parameters
indata = 'gnp.csv'

width = 600
height = 600

padding = 20
textpad = 10
tabpad = " "

fontsize = 12
titlefont = 16

w = width - 2*padding
h = height - 2*padding - titlefont - fontsize

line_width = 200


# styling for svg
css = """
    text {
        font-family: "Georgia", Georgia, serif;
    }
    """

# create svg
dwg = Drawing("test.svg", size=(width,height))
dwg.defs.add(dwg.style(css))

data = read_csv(indata)
labels = data.iloc[:,0]
cols = data.iloc[:,1:]

ncols = cols.shape[1]
nlines = ncols - 1
colspace = h - nlines*200
colwidth = colspace / float(ncols)
collocs = (arange(ncols) + 1)*colwidth

# pad
g = dwg.add(dwg.g(transform="translate(%i,%i)" % (padding,padding)))
title = g.add(dwg.g())

for i in range(ncols):
    if i==0:
        title.add(dwg.text(cols.columns[i], insert=(collocs[i],0), text_anchor='end', font_size='%ipx' % titlefont))
    elif i==ncols-1:
        title.add(dwg.text(cols.columns[i], insert=(collocs[i],0), font_size='%ipx' % titlefont))

g = g.add(dwg.g(transform="translate(0,%i)" % (titlefont+fontsize)))
# loop over and add labels
vmin = min(cols.values)
vmax = max(cols.values)

def scale(val, src=(vmin, vmax), dst=(0, h)):
    return ((float(val) - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def vertplace(j, col):
    val = col.iloc[j]
    if j > 0:
        prev = col.iloc[j-1]
        prevy = vertplace(j-1, col)
        curry = scale(val)

        diff = abs(curry-prevy)
        if diff < fontsize:
            return prevy - fontsize
        else:
            return curry
    else:
        return scale(val)

ys = {label: [] for label in labels}
for i in range(ncols):
    col = cols.iloc[:,i]
    
    sort = argsort(col)[::-1] # descending---top to bottom
    col = col[sort]
    collabels = labels[sort]

    for j in range(len(col)):
        val = col.iloc[j]
        y = vertplace(j, col)
        if i==0:
            txt = g.add(dwg.text(collabels.iloc[j]+tabpad+str(val), insert=(collocs[i], h - y), text_anchor='end', font_size="%ipx" % fontsize))
        elif i==ncols-1:
            txt = g.add(dwg.text(str(val)+tabpad+collabels.iloc[j], insert=(collocs[i], h - y), font_size="%ipx" % fontsize))
        else:
            txt = g.add(dwg.text(str(val), insert=(collocs[i], h - y), font_size="%ipx" % fontsize))

        ys[collabels.iloc[j]].append(y)

        if i > 0:
            line = g.add(dwg.line( (collocs[i-1]+textpad, h - ys[collabels.iloc[j]][i-1]), (collocs[i]-textpad, h - ys[collabels.iloc[j]][i]), stroke_width=1, stroke='black'))
    
dwg.save()
