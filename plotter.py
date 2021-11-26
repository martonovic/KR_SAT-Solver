import pdb
import matplotlib.pyplot as plt

def get_suduko_number(string):
    string = string.split('_')[-1].split('.')[0]
    if 't' in string[-2:]:
        return 'sudo'+string[-1]
    else:
        return 'sudo'+string[-2:]


def convert_str_to_list(string):
    string = string.replace('[', '').replace(']', '')
    string = string.split(',')
    if 'sudoku' in string[0]:
        string = [get_suduko_number(s) for s in string]
    else:
        string = [eval(s) for s in string ]
    return string


def get_key_value(line):
    key, value = line.split(':')[0], line.split(':')[-1]
    value = convert_str_to_list(value)
    return key, value

def get_points(file, metric_name):
    lines = file.readlines()
    lines[2] = lines[1].strip()+lines[2]
    lines = lines[2:]
    metric_dict = {}
    for line in lines:
        metric, values = get_key_value(line.strip())
        metric_dict[metric] = values
    
    return metric_dict[metric_name]
    


def boxplotter(metric_name):
    files = ['random_test_results_file.txt', 'DLIS_test_results_file.txt', 'JW_test_results_file.txt'] 
    labels = []
    all_data = []
    for file in files:
        heuristic_name = file.split('_')[0]
        f = open(file, 'r')
        labels.append(heuristic_name)
        data_points = get_points(f, metric_name)
        all_data.append(data_points)
        f.close()


    bplot = plt.boxplot(all_data, vert=True, patch_artist=True, labels=labels)
    plt.title('Runtime Comparision of Different SAT Heuristics')
        
    colors = ['pink', 'lightblue', 'lightgreen']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    plt.grid(True)
    plt.xlabel('SAT Heuristics')
    plt.ylabel(metric_name)
    plt.show()

boxplotter('Processing time in seconds')
