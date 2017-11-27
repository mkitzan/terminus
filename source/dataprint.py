import statistics


NVALID = "-"
ROUND = 4
SFUNCTS = {"Count": [0, lambda x: len(x)], "Unique": [1, lambda x: len(set(x))], 
           "Sum": [2, lambda x: sum(x)], "Minimum": [3, lambda x: NVALID if type(x[0]) is str else x[0]], 
           "Maximum": [4, lambda x: NVALID if type(x[-1]) is str else x[-1]], "Mean": [5, lambda x: round(statistics.mean(x), ROUND)], 
           "Median": [6, lambda x: statistics.median(x)], "Mode": [7, lambda x: statistics.mode(x)], 
           "Standard Deviation": [8, lambda x: round(statistics.stdev(x), ROUND)], "Variance": [9, lambda x: round(statistics.variance(x), ROUND)]}


def border(max_lens, edge):
    return "".join([edge + "-"*i for i in max_lens]) + edge


def printer(values, val_bufs):
    print("|" + "|".join([str(values[i]) + " " * val_bufs[i] for i in range(len(values))]) + "|")


def buffers(columns, values, buffer_val):
    max_lens = [len(str(i)) for i in columns]
    val_lens = [[i for i in max_lens]]

    for i in values:
        cur_lens = []
        for j in range(len(i)):
            cur_lens.append(len(str(i[j])))
            if cur_lens[j] > max_lens[j]:
                max_lens[j] = cur_lens[j]
        val_lens += [cur_lens]

    return [[max_lens[i]+buffer_val - el[i] for i in range(len(el))] for el in val_lens], [i+buffer_val for i in max_lens]


def print_data(tb_border, columns, values, val_bufs):
    print(tb_border)
    printer(columns, val_bufs[0])
    print(tb_border)

    for i in range(len(values)):
        printer(values[i], val_bufs[i + 1])

    print(tb_border)


def table(columns, values, edge="*", buffer_val=1):
    val_bufs, max_lens = buffers(columns, values, buffer_val)

    tb_border = border(max_lens, edge)

    print_data(tb_border, columns, values, val_bufs)
    

def process(values):
    stats = [[-1] for el in SFUNCTS.keys()]
    for key in SFUNCTS.keys():
        stats[SFUNCTS[key][0]] = [key]
    
    values = [list(el) for el in zip(*values)]
    
    for column in values:
        column.sort()
        
        for key in SFUNCTS.keys():
            try:
                stats[SFUNCTS[key][0]] += [SFUNCTS[key][1](column)]
            except:
                stats[SFUNCTS[key][0]] += [NVALID]

    return stats


def datastats(columns, values, edge="*", buffer_val=1, rounding=4, nvalid="-"):
    ROUND = rounding
    NVALID = nvalid
    
    values = process(values)
    
    if len(values[0]) == 1:
        for i in range(len(values)):
            values[i] += [nvalid] * len(columns)
    
    columns = ["Statistics"] + columns
    
    table(columns, values, edge, buffer_val)
