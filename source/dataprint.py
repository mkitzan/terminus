import math


def border(max_lens, edge):
    return "".join([edge + "-"*i for i in max_lens]) + edge


def printer(values, val_bufs):
    print("|" + "|".join([str(values[i]) + " " * val_bufs[i] for i in range(len(values))]) + "|")


def buffers(columns, values, buffer):
    max_lens = [len(str(i)) for i in columns]
    val_lens = [[i for i in max_lens]]

    for i in values:
        cur_lens = []
        for j in range(len(i)):
            cur_lens.append(len(str(i[j])))
            if cur_lens[j] > max_lens[j]:
                max_lens[j] = cur_lens[j]
        val_lens.append(cur_lens)

    return [[max_lens[i]+buffer - el[i] for i in range(len(el))] for el in val_lens], [i+buffer for i in max_lens]


def print_data(tb_border, columns, values, val_bufs):
    print(tb_border)
    printer(columns, val_bufs[0])
    print(tb_border)

    for i in range(len(values)):
        printer(values[i], val_bufs[i + 1])

    print(tb_border)


def table(columns, values, edge="*", buffer=1):
    val_bufs, max_lens = buffers(columns, values, buffer)

    tb_border = border(max_lens, edge)

    print_data(tb_border, columns, values, val_bufs)


def process(values, decimals=4):
    types = ["t" if type(el) is str else "n" for el in values[0]]

    stats = [["Count"], ["Unique"], ["Sum"], ["Average"], ["Standard Deviation"], ["Minimum"], ["Maximum"]]
    temp_min = 0
    temp_max = 99999
    col_space = len(types)

    count = [len(values)] * col_space
    unique = [[] for i in range(col_space)]
    sum_val = [temp_min] * col_space
    sd = [temp_min] * col_space
    max_val = [temp_min] * col_space
    min_val = [temp_max] * col_space

    for row in values:
        for i in range(len(row)):
            if types[i] == "n":
                sum_val[i] += int(row[i])

                if row[i] > max_val[i]:
                    max_val[i] = row[i]

                if row[i] < min_val[i]:
                    min_val[i] = row[i]

            if str(row[i]) not in unique[i]:
                unique[i].append(str(row[i]))

    for i in range(col_space):
        stats[0] += [count[i]]
        stats[1] += [len(unique[i])]
        stats[2] += ["-"] if sum_val[i] == temp_min else [sum_val[i]]
        stats[3] += [round(sum_val[i] / count[i], decimals)] if types[i] == "n" else ["-"]
        stats[5] += ["-"] if min_val[i] == temp_max else [min_val[i]]
        stats[6] += ["-"] if max_val[i] == temp_min else [max_val[i]]

    for row in values:
        for i in range(len(row)):
            if types[i] == "n":
                sd[i] += math.pow(int(row[i]) - float(stats[3][i+1]), 2)
    stats[4] += [round(math.sqrt(sd[i] / count[i]), decimals) if types[i] == "n" else "-" for i in range(col_space)]

    return stats


def statistics(columns, values, edge="*", buffer=1):
    columns = ["Statistics"] + columns
    values = process(values)
    val_bufs, max_lens = buffers(columns, values, buffer)
    
    tb_border = border(max_lens, edge)

    print_data(tb_border, columns, values, val_bufs)
