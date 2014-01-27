Tufte Slopegraphs
=================

A D3.js, LaTeX take on [this Edward Tufte
challenge](http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0003nk)

`slopegraph.py` will generate a D3.js document and a LaTeX file containing
slope graphs of input data, with a specified title.

`svg.py`
--------
`svg.py` contains code that generates the SVG image `test.svg`. This
implements a two-column slopegraph, to be embedded in a document with
a title, etc.

`slopegraph.py`
---------------
User specifies two items in `slopegraph.py`: `filename` and `title`.

`filename` specifies a source data file, which is comma separated with three
columns:

1. `label`: Item label
2. `col1`: Column 1, titled "col1" (or whatever)
3. `col2`: Column 2, title "col2"

`title`, appropriately, gives the title of the chart.

Formats
-------
To convert SVG to PNG, see [Mike
Bostock](http://bl.ocks.org/mbostock/6466603).
