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

filename = "gnp.csv"
title = "Current Receipts of Government as a Percentage of Gross Domestic Product, 1970 and 1979"
data = json_csv(filename)

def plot_slopegraph(data_dict, normalize=1):
    """
        Function to generate plot; takes dictionary in form
            {country1: {year1: val1, year2: val2, year3:val3,...}, ...}
        Allows for N countries and T years

        Plot will have an average level in the middle
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

    # Generate figure 
    fig, ax = plt.subplots()
    x_vals = range(2 + len(years))
    x_labs = len(x_vals) * ['']

    
    # Plot each, looping first through obs, then through time
    for i, obs_name in enumerate(obs_names):
        
        for j, year in enumerate(years):
            x_plot = [x_vals[j+1]]
            y_plot = data_mat[i, j]

            ax.plot(x_plot, y_plot, 'wo')

            if j == 0:
                ax.text(x_plot, y_plot, obs_name + ' ', 
                        horizontalalignment='right')
            elif j == T:
                ax.text(x_plot, y_plot, ' ' + obs_name, 
                        horizontalalignment='left')


    # Plot the average more conspicuously
    for i, year in enumerate(years):
        x_plot = [x_vals[i+1]]
        y_plot = data_mat[-1, i]

        ax.plot(x_plot, y_plot, 'bo')
    
    ax.set_xticks(x_vals)
    ax.set_xticklabels(x_labs)
    print x_labs
    plt.show()



        
        



