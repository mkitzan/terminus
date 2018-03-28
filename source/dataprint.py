import statistics
import theme

from shutil import get_terminal_size
from time import strftime
from math import ceil


# default parameters for tables and exports
WINDOW = 180
PATH = "reports/"
NVALID = "-"
MISSING = "Not Provided"
ROUND = 4

# statistic functions for the stats table
SFUNCTS = {"Total": [0, lambda x: len(x)], 
           "Unique": [1, lambda x: len(set(x))],
           "Sum Total": [2, lambda x: sum(x)], 
           "Sum Unique": [3, lambda x: sum(set(x))],
           "Minimum": [4, lambda x: NVALID if type(x[0]) is str else x[0]],
           "Maximum": [5, lambda x: NVALID if type(x[-1]) is str else x[-1]],
           "Mean": [6, lambda x: round(statistics.mean(x), ROUND)],
           "Median": [7, lambda x: int(statistics.median(x)) if type(x[0]) is int else statistics.median(x)], 
           "Mode": [8, lambda x: statistics.mode(x)],
           "Standard Deviation": [9, lambda x: round(statistics.stdev(x), ROUND)], 
           "Variance": [10, lambda x: round(statistics.variance(x), ROUND)]}

# aggregate functions to plot by
PLOT_OPS = {"count": lambda arr: len(set(arr)),
            "sum": lambda arr: sum(arr),
            "avg": lambda arr: sum(arr) / len(arr)}
            
            
def set_max_y(res, flg, max_y):
    """Tests/sets max length of y-axis values."""
    test = res[-1][1 if flg == "y" else 0]
    
    if (len(str(test)) if type(test) is str else test) > max_y:
        max_y = len(str(test)) if type(test) is str else test
    
    return max_y


def set_max_x(res, flg, max_x):
    """Tests/sets max length of x-axis values."""
    test = res[-1][1 if flg == "x" else 0]

    if (len(str(test)) if type(test) is str else test) > max_x:
        max_x = len(str(test)) if type(test) is str else test

    return max_x
    
    
def plot_aggregate_x(columns, res, max_y, max_x, buffer_val, point, scale, op, funct):
    """Prints the graph for queries aggregated over the x-axis."""
    # graph legend
    funct(" " * (max_y) + "X-axis: " + op + "(" + columns[1] + ")" + "   Scale: " + str(scale) + "   Y-axis: " + columns[0])
    
    # graph body
    for el in res:
        funct((((" " * max_y) + "|\n") * buffer_val) + (" " * (max_y - len(el[0]))) + el[0] + "|" + (point * el[1]))
    
    # x-axis
    funct(" " * (max_y+1) + "-" * max_x)
    
    # x-axis labels
    for i in range(len(str(max_x+1))):
        funct((" " * (max_y+1)) + "".join([((str(el)[i] + (" " * buffer_val)) if len(str(el)) > i else (" " * (buffer_val+1))) for el in range(1, max_x+1)]))
        
        
def plot_aggregate_y(columns, res, max_y, max_x, buffer_val, point, scale, op, funct):
    """Prints the graph for queries aggregated over the y-axis."""
    # graph legend
    funct(" " * (len(str(max_y))+1) + "X-axis: " + columns[0] + "   Y-axis: " + op + "(" + columns[1] + ")" + "   Scale: " + str(scale))

    # creates a list of (value, 'buffer offset') pairs
    res = [[el[0],(max_y - el[1])] for el in res]

    # graph body
    for i in range(1, max_y+1):
        st = " " * (len(str(max_y)) - len(str(max_y+1 - i))) + str((max_y+1) - i) + "|"
        for el in res:
            st += (" " if i <= el[1] else point) + (" " * buffer_val)
        funct(st)
    
    # x-axis
    funct(((len(str(max_y))+1) * " ") + ("-" * (len(st) - len(str(max_x)) - (1 + buffer_val))))
    
    # x-axis labels
    for i in range(max_x):
        funct(((len(str(max_y))+1) * " ") + "".join([(str(el[0][i]) + (" " * buffer_val)) if len(el[0]) > i else (" " * (buffer_val+1)) for el in res]))

    
def plot(columns, results, op, scale, flg, point="*", buffer_val=0, funct=print):
    """Process results set and args for printing a graph."""
    res = []
    temp = []
    max_x = -1
    max_y = -1
    num = False
    verbose = False
    
    try:
        curr = int(results[0][0])
        num = True
    except ValueError:
        if columns[0] in theme.VERBOSE:
            verbose = True
            
        curr = results[0][0]
    
    # performs sum, count, or avg function for each distinct record value as a key
    for el in results:
        if el[0] != curr:
            if verbose:
                curr = " ".join([ch for ch in curr])
                
            res += [[str(curr) if num else "".join([word[0] for word in curr.split(" ")]), round(PLOT_OPS[op](temp) / scale)]]    
            max_y = set_max_y(res, flg, max_y)
            max_x = set_max_x(res, flg, max_x)
                
            curr = int(el[0]) if num else el[0]
            temp = []
        temp += [el[-1]]
    
    if verbose:
        curr = " ".join([ch for ch in curr])
        
    res += [[str(curr) if num else "".join([word[0] for word in curr.split(" ")]), round(PLOT_OPS[op](temp) / scale)]]
    max_y = set_max_y(res, flg, max_y)
    max_x = set_max_x(res, flg, max_x)
    
    if columns[0] in theme.SPEC_SORT:
        sortby = theme.SPEC_SORT[columns[0]]
        res.sort(key=lambda item: sortby.index(item[0]))
    
    if funct == print:
        print()
        
    if flg == "x":
        plot_aggregate_x(columns, res, max_y, max_x, buffer_val, point, scale, op, funct)
        
    elif flg == "y":
        plot_aggregate_y(columns, res, max_y, max_x, buffer_val, point, scale, op, funct)
            

def borders(max_lens, point):
    """Creates horizontal borders for the results table."""
    cols, rows = get_terminal_size()
    
    top_border = bot_border = tb_border = "".join([point + "-"*i for i in max_lens]) + point
    breaks = []
    
    if cols < len(tb_border):
        start = cols * (len(breaks) + 1)
        i = 0
        
        while start < len(tb_border):
            if tb_border[start-i] == point:
                breaks += [start-i+1]
                start = cols * (len(breaks) + 1)
                i = -1
            i += 1
            
        top_border = tb_border[:breaks[0]]
        bot_border = tb_border[breaks[-1]:]
        
    return breaks, top_border, bot_border


def make_row(values, val_bufs, breaks=[]):
    """Creates a row for the results table."""
    row = "|" + "|".join([str(values[i]) + " " * val_bufs[i] for i in range(len(values))]) + "|"

    for i in range(len(breaks)):
        row = row[:breaks[i]+i] + "\n" + row[breaks[i]+i:]
        
    return row


def buffers(columns, values, buffer_val):
    """Processes the space multiple for buffers between records value and column borders."""
    max_lens = [len(str(i)) for i in columns]
    val_lens = [[i for i in max_lens]]

    for i in values:
        cur_lens = []
        
        for j in range(len(i)):
            cur_lens += [len(str(i[j]))]
            
            if cur_lens[j] > max_lens[j]:
                max_lens[j] = cur_lens[j]
            
        val_lens += [cur_lens]

    return [[max_lens[i]+buffer_val - el[i] for i in range(len(el))] for el in val_lens], [i+buffer_val for i in max_lens]


def print_data(breaks, top_border, bot_border, columns, values, val_bufs, funct):
    """Creates the actual table from the processed data."""
    funct(top_border + "\n" + make_row(columns, val_bufs[0], breaks) + "\n" + bot_border)

    for i in range(len(values)):
        funct(make_row(values[i], val_bufs[i+1], breaks))

    funct(bot_border)


def table(columns, values, point="*", buffer_val=1, funct=print):
    """Calls functions to prepare for printing."""
    val_bufs, max_lens = buffers(columns, values, buffer_val)
    
    breaks, top_border, bot_border = borders(max_lens, point)

    if funct == print:
        print()
        
    print_data(breaks, top_border, bot_border, columns, values, val_bufs, funct)
    

def process(values, columns):
    """Processes statistic values for each column in the results set."""
    # creates a list to store stats results
    stats = [[-1] for el in SFUNCTS.keys()]
    for key in SFUNCTS.keys():
        stats[SFUNCTS[key][0]] = [key]
    
    # transposes results set
    values = [list(el) for el in zip(*values)]
    
    for column in values:
        column.sort()
        
        for key in SFUNCTS.keys():
            try:
                stats[SFUNCTS[key][0]] += [SFUNCTS[key][1](column)]
            # case where the value is not a number
            except Exception:
                stats[SFUNCTS[key][0]] += [NVALID]
    
    # catches case where results set is empty
    if len(stats[0]) == 1:
        for i in range(len(stats)):
            stats[i] += [NVALID] * len(columns)
    
    columns = ["Statistic"] + columns

    return stats, columns


def stats(columns, values, point="*", buffer_val=1, remainder=4, nvalid="-", funct=print):
    """Calls functions to process statistics, and print the table."""
    ROUND = remainder
    NVALID = nvalid
    
    values, columns = process(values, columns)
    
    table(columns, values, point, buffer_val, funct)
    
    
def exp_plot(x, y, columns, values, op, scale, axis, buffer_val, fnct):
    """Plot helper function for 'export'. Formats results for plotting."""
    temp = [values[columns.index(x)], values[columns.index(y)]]
    temp = sorted([list(el) for el in zip(*temp)], key=lambda x: x[0])
    plot([x, y], temp, op, scale, axis, buffer_val=1, funct=fnct)
    
    fnct("")


def export(columns, values, tb=MISSING, args=MISSING, point="*", buffer_val=1, remainder=4, nvalid="-", source=theme.SOURCE):
    """Creates and writes data to export file. 
    Export file includes: result set table, statistics table, and four different graphs."""
    ROUND = remainder
    NVALID = nvalid
    
    expfile = open(PATH + strftime("%m-%d-%Y") + " " + source + ".txt", "w+")
    expfile.write(strftime(theme.DATE_TIME + " %H:%M:%S") + theme.LABEL_TB + tb + theme.LABEL_ARGS + args + theme.LABEL_RSET)    
    table(columns, values, point, buffer_val, lambda x: expfile.write(x + "\n"))
    
    expfile.write(theme.LABEL_RSTATS)
    stats(columns, values, point, buffer_val, remainder, nvalid, lambda x: expfile.write(x + "\n"))
    
    if theme.REPORTS[source] != []:
        # transpose graph correctly, change 'y' -> 'x', and buffer_val=0
        values = [list(el) for el in zip(*values)]
        expfile.write("\n")

        # plot / write the pre-set report graphs from within the theme file
        for group in theme.REPORTS[source]:
            expfile.write(theme.GRAPH_HEADER+group[0])

            for graph in group[1:]:
                exp_plot(graph[0], graph[1], columns, values, graph[2], graph[3], graph[4], graph[5], lambda x: expfile.write(x + "\n"))
        
    expfile.close()
