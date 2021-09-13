import csv
from collections import defaultdict
import numpy as np
import csep
from csep.utils import time_utils
import matplotlib.pyplot as pyplot
import matplotlib.transforms as trans
from matplotlib.lines import Line2D
from scipy.stats import norm


def prune_test_distribution(result):
    del result.test_distribution

def read_zechar_csv_to_dict(zechar_truth_path):
    """ Reads csv file storing zechar truth into dict """
    output = defaultdict(dict)
    with open(zechar_truth_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            results = {}
            first = True
            for k, v in row.items():
                # we expect first column to store model name
                if first:
                    name = v
                    first = False
                # else, key contains test name, with exception of n-test that is stored as n-test1 and n-test2
                else:
                    results[k] = v
            first = True
            output[name] = results
    return output



def plot_consistency_test_comparison(results_dict, zechar_dict):
    """ Plots figure for between pyCSEP results and Zechar et al. (2013) results.

        There are expectations about the keys in the two dictionaries. The keys in results_dict should be
        the same as the header values of zechar_truth. the first column of zechar_truth should contain the 
        model name that is stored in the evaluation_result.

        Args:
            results_dict (dict): contains evaulation results with dict[key] is list of result objects
            zechar_dict (dict): contains values from zechar et al. (2013)

        Returns:
            axes (matplotlib.Axes): matplotlib axes objects
    """
    results_dict_formatted = defaultdict(dict)
    # convert results format into identical dict structure from zechar_dict
    for eval_name, results_list in results_dict.items():
        for result in results_list:
            if eval_name == 'n-test':
                results_dict_formatted[result.sim_name]['n-test1'] = result.quantile[0]
                results_dict_formatted[result.sim_name]['n-test2'] = result.quantile[1]
            else:
                results_dict_formatted[result.sim_name][eval_name] = result.quantile

    # create figure
    xtick_labels = []
    xticks = []
    legend_entries = []
    points_per_inch = 72
    markersize=45
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:purple', 'tab:red', 'tab:cyan']
    symbols = ['o','s','^','*','h','>']
    fig, ax = pyplot.subplots(figsize=(7, 7))
    ax.axhline(y=0, linestyle='--', color='black', alpha=0.3)
    num_sims = len(results_dict_formatted)
    first = True
    all_diffs = []
    pycsep_quantiles = []
    zechar_quantiles = []
    for i, (sim_name, eval_result_dict) in enumerate(zechar_dict.items()):
        xticks.append(i+1)
        xtick_labels.append(sim_name)
        for j, (eval_name, zechar_quantile) in enumerate(eval_result_dict.items()):
            pycsep_quantile = results_dict_formatted[sim_name][eval_name]
            # signed difference 
            try:
                if eval_name == 'n-test1' or eval_name == 'n-test2':
                    pycsep_quantile = round(pycsep_quantile, 3)
                else:
                    pycsep_quantile = round(pycsep_quantile, 6)
                ratio = float(pycsep_quantile) - float(zechar_quantile)
            except:
                pass
            pycsep_quantiles.append(float(pycsep_quantile))
            zechar_quantiles.append(float(zechar_quantile))
            all_diffs.append(ratio)
            # define transform to plot markers adjacent to one another
            dx, dy = markersize / points_per_inch / 6, 0
            h = num_sims / 2
            offset = trans.ScaledTranslation(dx*(j-h), dy, fig.dpi_scale_trans)
            offset_trans = ax.transData + offset
            # plot
            ax.scatter(i+1, ratio, s=markersize, transform=offset_trans, color=colors[i], marker=symbols[j])
            if first:
                entry = Line2D([0],[0], marker=symbols[j], label=eval_name, color='gray', markerfacecolor='gray', markersize=8, lw=0)
                legend_entries.append(entry)
        first=False
    abs_diff = np.array(all_diffs).mean()
    print(f'Avg. diff: {abs_diff}')
    npyq = len(pycsep_quantiles)
    nzeq = len(zechar_quantiles)
    df = npyq - 1
    # assume errors are ~N(0, std(diffs))
    mu = 0.0
    # unbiased estimate; mle for norm. var. use ddof=0
    sp = np.std(all_diffs) / np.sqrt(npyq)
    n2p5 = norm.ppf(0.025, mu, sp)
    n97p5 = norm.ppf(0.975, mu, sp)
    ax.fill_between(np.arange(npyq), n2p5, y2=n97p5, alpha=0.2, color='gray')
    # Plot formatting
    ax.set_xticks(xticks)
#     ax.set_yticks(np.arange(-0.1, 1.05, 0.05))
    ax.set_xticklabels(xtick_labels, rotation=-45, ha='left')
    ax.set_xlim([0.25, num_sims+.75])
    ax.set_ylim([-0.005, 0.005])
    ax.tick_params(axis='both', labelsize=14)
    ax.set_ylabel('Quantile score error', fontsize=16)
    
    # Create custom legend
    ax.legend(handles=legend_entries, loc='upper right', fontsize=14)
    ax.get_figure().tight_layout()
    return ax

def load_zechar_catalog(filename):
    """ Loads catalog as presented by Table 1 in Zechar et al., 2013 """

    month_str_to_num = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    eventlist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            # event_id
            event_id = line[0]
            # day of month
            day = line[1]
            # month
            month_str = line[2]
            month = month_str_to_num[month_str]
            # year
            year = line[3]
            # time string
            time = line[4]
            # create origin time
            time_string = "{0}-{1}-{2} {3}".format(year, month, day, time)
            origin_time = time_utils.strptime_to_utc_epoch(time_string, format="%Y-%m-%d %H:%M")
            # latitude
            latitude = float(line[5])
            # longitude
            longitude = float(line[6])
            # magnitude
            magnitude = float(line[7])
            # depth
            depth = float(line[8])
            event_tuple = (
                event_id,
                origin_time,
                latitude,
                longitude,
                depth,
                magnitude
            )
            eventlist.append(event_tuple)

    return eventlist
