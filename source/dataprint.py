import statistics

from time import strftime


PATH = ""
NVALID = "-"
MISSING = "Not Provided"
ROUND = 4
SFUNCTS = {"Total": [0, lambda x: len(x)], "Unique": [1, lambda x: len(set(x))],
           "Sum Total": [2, lambda x: sum(x)], "Sum Unique": [3, lambda x: sum(set(x))],
           "Minimum": [4, lambda x: NVALID if type(x[0]) is str else x[0]],
           "Maximum": [5, lambda x: NVALID if type(x[-1]) is str else x[-1]],
           "Mean": [6, lambda x: round(statistics.mean(x), ROUND)],
           "Median": [7, lambda x: statistics.median(x)], "Mode": [8, lambda x: statistics.mode(x)],
           "Standard Deviation": [9, lambda x: round(statistics.stdev(x), ROUND)], 
           "Variance": [10, lambda x: round(statistics.variance(x), ROUND)]}


def border(max_lens, edge):
    return "".join([edge + "-"*i for i in max_lens]) + edge


def make_row(values, val_bufs):
    return "|" + "|".join([str(values[i]) + " " * val_bufs[i] for i in range(len(values))]) + "|"


def buffers(columns, values, buffer_val):
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


def print_data(tb_border, columns, values, val_bufs, funct):
    funct(tb_border + "\n" + make_row(columns, val_bufs[0]) + "\n" + tb_border)

    for i in range(len(values)):
        funct(make_row(values[i], val_bufs[i + 1]))

    funct(tb_border)


def table(columns, values, edge="*", buffer_val=1, funct=print):
    val_bufs, max_lens = buffers(columns, values, buffer_val)

    tb_border = border(max_lens, edge)

    print_data(tb_border, columns, values, val_bufs, funct)
    

def process(values, columns):
    stats = [[-1] for el in SFUNCTS.keys()]
    for key in SFUNCTS.keys():
        stats[SFUNCTS[key][0]] = [key]
    
    values = [list(el) for el in zip(*values)]
    
    for column in values:
        column.sort()
        
        for key in SFUNCTS.keys():
            try:
                stats[SFUNCTS[key][0]] += [SFUNCTS[key][1](column)]
            except Exception:
                stats[SFUNCTS[key][0]] += [NVALID]

    if len(stats[0]) == 1:
        for i in range(len(stats)):
            stats[i] += [NVALID] * len(columns)
    
    columns = ["Statistic"] + columns

    return stats, columns


def stats(columns, values, edge="*", buffer_val=1, remainder=4, nvalid="-", funct=print):
    ROUND = remainder
    NVALID = nvalid
    
    values, columns = process(values, columns)
    
    table(columns, values, edge, buffer_val, funct)
    
    
def export(columns, values, tb=MISSING, args=MISSING, edge="*", buffer_val=1, remainder=4, nvalid="-"):
    ROUND = remainder
    NVALID = nvalid
    
    print("    Status [1/3]: creating file, and writing header to file")
    
    expfile = open(PATH + strftime("%d-%m-%Y") + " DB Export.txt", "w+")
    expfile.write(strftime("%d/%m/%Y %H:%M:%S") + "\n\nHost Table: " + tb + "\nArguments: " + args + "\n\nResults Set\n")
    
    print("    Status [2/3]: writing results set to file")
    
    table(columns, values, edge, buffer_val, lambda x: expfile.write(x + "\n"))
    
    print("    Status [3/3]: writing statistics to file")
    
    expfile.write("\nResults Statistics\n")
    stats(columns, values, edge, buffer_val, remainder, nvalid, lambda x: expfile.write(x + "\n"))
    
    expfile.close()
