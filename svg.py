from svgwrite import Drawing
from pandas import read_csv
from numpy import min, max, arange

# parameters
indata = 'gnp.csv'

width = 600
height = 600

padding = 20
textpad = 10
tabpad = " "

w = width - 2*padding
h = height - 2*padding

line_width = 200

# styling for svg
css = """
    text {
        font-family: "Georgia", Georgia, serif;
        font-size: 12px;
    }
    """

# create svg
dwg = Drawing("test.svg", size=(width,height))
dwg.defs.add(dwg.style(css))
# pad
g = dwg.add(dwg.g(transform="translate(%i,%i)" % (padding,padding)))

data = read_csv(indata)
labels = data.iloc[:,0]
cols = data.iloc[:,1:]

ncols = cols.shape[1]
nlines = ncols - 1
colspace = h - nlines*200
colwidth = colspace / float(ncols)
collocs = (arange(ncols) + 1)*colwidth

# loop over and add labels
vmin = min(cols.values)
vmax = max(cols.values)

def scale(val, src=(vmin, vmax), dst=(0, h)):
    return ((float(val) - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

for i in range(len(cols)):
    row = cols.iloc[i,:]
    for j in range(ncols):
        y = scale(row[j])
        if j==0:
            txt = g.add(dwg.text(labels[i]+tabpad+str(row[j]), insert=(collocs[j], h - y), text_anchor="end"))
        elif j==ncols-1:
            txt = g.add(dwg.text(str(row[j])+tabpad+labels[i], insert=(collocs[j], h - y)))
        else:
            txt = g.add(dwg.text(str(row[j]), insert=(collocs[j], h - y)))

        if j > 0:
            line = g.add(dwg.line( (collocs[j]-textpad, h - y), (collocs[j-1]+textpad, h - scale(row[j-1])), stroke_width=1, stroke='black'))
    
dwg.save()
