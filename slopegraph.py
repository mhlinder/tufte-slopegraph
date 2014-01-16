# http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0003nk
import numpy as np
import matplotlib.pyplot as plt

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

    
def scale(val, src, dst):
    return ((float(val) - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


def vertplace(j, col, fontsize):
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


def plot_slopegraph(data_dict, title, normalize=0):
    """
        Function to generate plot; takes dictionary in form
            {country1: {year1: val1, year2: val2, year3:val3,...}, ...}
        Allows for N countries and T years

        Plot will have an average level in the middle.

    """

    # Get basic stats to use for plotting, labeling, making
    #   data structures
    obs_names = data_dict.keys()
    N = len(obs_names)
    T = len(data_dict[obs_names[0]])
    years = data_dict[obs_names[0]].keys()
    years.sort()

    # Construct array object to hold plotting data
    #   N+1 because will add mean
    data_mat = np.zeros((N+1, T))
    data_mat[:] = np.nan

    # Loop over countries and put them in matrix array
    for i, obs_name in enumerate(obs_names):
        obs_data = data_dict[obs_name]
        for j, year in enumerate(years):
            data_mat[i, j] = obs_data[year]

    # Normalize 
    if normalize:
        baseyr_data = data_mat[:, 0]
        baseyr_ave = baseyr_data[~np.isnan(baseyr_data)].mean()
        data_mat = data_mat / baseyr_ave

    # Add column average as final observation 
    for i, year in enumerate(years):
        data_mat[N, i] =  data_mat[~np.isnan(data_mat)[:, i], i].mean()

    # Add col to hold ind var for average
    data_mat = np.hstack((data_mat, np.zeros((N+1,1))))
    data_mat[N, T] = 1

    # Get a new matrix to hold the location of the text values,
    #   which we will have to change given spacing/overlap considerations
    data_mat.sort(axis=0)
    text_locs = np.copy(data_mat) 


    ## PLOTTING ##

    # General figure settings
    fig, ax = plt.subplots(facecolor='white', figsize=(6,8),
            dpi=80)

    x_labs = [''] + years + ['']
    for ind, lab in enumerate(x_labs): x_labs[ind] = '\n' + str(lab)
    x_vals = range(len(x_labs))
    

    # Plot each, looping first through obs, then through time
    for i, obs_name in enumerate(obs_names):

        # Color based on whether the indicator column is 1
        if data_mat[i,T] == 1:
            color = '-b'
        else:
            color = '-k'


        # Plot observation
        ax.plot(x_vals[1:-1], data_mat[i, 0:-1], color)


        # Add text labels
        aligns = ['right', 'left']
        labels = [obs_name + ' ' + str(round(data_mat[i,1], 2)),
                    str(round(data_mat[i,T-1],2)) + ' ' + obs_name]
        for ind, t in enumerate([1, T]):
            ax.text(x_vals[t], data_mat[i,t-1], labels[ind], 
                    horizontalalignment=aligns[ind], 
                    verticalalignment='center')

    ax.set_title(title)
    ax.set_xticks(x_vals)
    ax.set_xticklabels(x_labs, fontsize='16')
    ax.set_frame_on(False)
    ax.tick_params(axis='both', which='both', left='off', right='off',
            labelleft='off', bottom='off', top='off', pad=10)

    plt.show()


# Pull in data
filename = "gnp.csv"
title = "Current Receipts of Government as a Percentage of Gross Domestic Product, 1970 and 1979"
data = json_csv(filename)

# Plot
a = plot_slopegraph(data, 'Country Comparison')



