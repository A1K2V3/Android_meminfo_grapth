import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import xml.etree.ElementTree as ET
from matplotlib.ticker import ScalarFormatter


def init_plotting():
    plt.rcParams['figure.figsize'] = (14,8)
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] =  plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['savefig.dpi'] = plt.rcParams['savefig.dpi']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = False
    plt.rcParams['legend.loc'] = 'center left'
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['axes.formatter.useoffset'] = False
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')

#function to parse xml file
def parse_xml(xmlfile):
    pkg_name, color_scheme, times_minu, graphs = [], [], [], []
    filename, max_memory = '', ''
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    for child in root:
        if child.tag == "package":
            for pkg in child:
                pkg_name.append(pkg.text)
        elif child.tag == "color":
            for color in child:
                color_scheme.append(color.text)
        elif child.tag == "time":
            for times in child:
                times_minu.append(int(times.text.strip()))
        elif child.tag == "graph":
            for graph in child:
                graphs.append(graph.text)
        elif child.tag == "file_name":
            filename = child.text
        elif child.tag == "max_memory":
            max_memory = int(child.text.strip())
    return pkg_name, color_scheme, times_minu, graphs, filename, max_memory

#function to filter out meminfo file
def filter_meminfo(filename,package_name):
    var = []
    with open(filename, "r") as infile:
        for line in infile:
            if package_name in line:
                var.append(line.split(":")[0].split("K")[0].strip())
    value = [float(i.replace(",","")) for i in var]
#    value = [float(i) for i in var if i]
    value = np.array(value[::2])
    index = np.array([i for i,_ in enumerate(value)])
    return index,value

#function to plot graphs
def plot_graph(graph_type, index, value, clr, time_max, mem_max, pkg_name):
    plt.axis([0, time_max, 0, mem_max])
    plt.xlabel("Time in minutes")
    plt.title("Memory Leak Graph ")
    plt.tight_layout()
    plt.grid(True)
    if graph_type == "plot":
        plt.plot(index, value, linestyle="-", marker=".", linewidth=1, color=clr, label=pkg_name)
        plt.savefig(pkg_name.replace(".", "_")+"_" + time.strftime("%Y-%m-%d") + '.png')
    elif graph_type == "scatter":
        plt.scatter(index, value, marker="o", color=clr, label=pkg_name)
        plt.savefig(pkg_name.replace(".", "_")+ "_"+ time.strftime("%Y-%m-%d") + '.png')

#main function
def func():
    style.use('ggplot')
    init_plotting()
    pkg_name, color_scheme, time_minu, graphs, filename, max_memory = parse_xml("plotgraph.xml")
    for index,name in enumerate(pkg_name):
        time_index, value = filter_meminfo(filename, name)
        if graphs[1] == 'single':
            plot_graph(graphs[0], time_index, value, color_scheme[index],time_minu[0], max_memory, name)
        elif graphs[1] == 'multiple':
            plot_graph(graphs[0], time_index, value, color_scheme[index], time_minu[0], max_memory, name)
            plt.text(0.48 * time_minu[0], 0.9 * max_memory,"Max. Mem:" + str(value.max()), horizontalalignment='center',verticalalignment='center',color="r")
            plt.ylabel(name)
            plt.show()
    if graphs[1] == 'single':
        plt.legend(loc='upper left')
        plt.show()

if __name__ == '__main__':
    func()
