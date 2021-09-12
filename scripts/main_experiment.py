# imports
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as pyplot

# pycsep imports
import csep
from csep.utils import stats, plots

# experiment imports
from experiment_utilities import (
        load_zechar_catalog,
        plot_consistency_test_comparison,
        read_zechar_csv_to_dict
)
from experiment_config import config


# runtime flags
show_target_event_rates = True
plot = False
compute_evaluations = True

# catalog from manuscript
catalog = csep.load_catalog('./data/evaluation_catalog_zechar2013_merge.txt', loader=load_zechar_catalog)
evaluation_results = defaultdict(list)

# load results from zechar
zechar_dict = read_zechar_csv_to_dict('./data/consistency_quantile_scores_from_zechar.csv')

# main evaluation loop
for name, path in config['forecasts'].items():

    # load forecast
    fore = csep.load_gridded_forecast(
            config['forecasts'][name],
            start_date=config['start_date'],
            end_date=config['end_date'],
            name=name
    )

    # assign region of forecast to catalog
    catalog.region = fore.region
    cat_filt = catalog.filter_spatial(in_place=False)
    
    # assign region to new catalog
    cat_filt.region = fore.region

    # compute likelihood and expected number of events
    spatial_magnitude_counts = cat_filt.spatial_magnitude_counts()
    ll = stats.poisson_log_likelihood(spatial_magnitude_counts, fore.data).sum()

    # print summary statistics
    print(f"{name}\n==========================")
    print(f"Nfore: {fore.sum()}\nNobs: {cat_filt.event_count}\nLL/Nobs: {ll / cat_filt.event_count}")
    print("")

    if show_target_event_rates:
        print("Target event rates")
        for lon, lat, mag in zip(cat_filt.get_longitudes(), cat_filt.get_latitudes(), cat_filt.get_magnitudes()):
            try:
                rate = fore.get_rates([lon], [lat], [mag])
                print(lon, lat, mag, rate[0])
            except ValueError:
                print(lon, lat, mag, "ERROR")
        print("")

    # n-test
    if compute_evaluations:
        n_test_result = csep.poisson_evaluations.number_test(
            fore, 
            cat_filt
        )
        evaluation_results['n-test'].append(n_test_result)
        print(f"N-test result: {n_test_result.quantile}")

        # m-test
        m_test_result = csep.poisson_evaluations.magnitude_test(
            fore, 
            cat_filt, 
            num_simulations=config['nsims'],
            seed=config['seed']
        )
        evaluation_results['m-test'].append(m_test_result)
        print(f"M-test result: {m_test_result.quantile}")

        # s-test
        s_test_result = csep.poisson_evaluations.spatial_test(
            fore, 
            cat_filt, 
            num_simulations=config['nsims'],
            seed=config['seed'],
        )
        evaluation_results['s-test'].append(s_test_result)
        print(f"S-test result: {s_test_result.quantile}")

        # l-test
        l_test_result = csep.poisson_evaluations.likelihood_test(
            fore, 
            cat_filt, 
            num_simulations=config['nsims'],
            seed=config['seed'],
        )
        evaluation_results['l-test'].append(l_test_result)
        print(f"L-test result: {l_test_result.quantile}")
        print("")

# plot and save results
ax = plot_consistency_test_comparison(evaluation_results, zechar_dict)
ax.get_figure().savefig('./output/pycsep_zechar_comparison.pdf')

# visualizations
if plot:
    ax = plots.plot_poisson_consistency_test(
        evaluation_results['n-test'], 
        plot_args={'xlabel': 'Observed earthquakes'}
    )
    ax.set_xlim([0,100])
    ax.get_figure().savefig('./output/number_test_pycsep.pdf')

    ax = plots.plot_poisson_consistency_test(
        evaluation_results['l-test'], 
        plot_args={'xlabel': 'log-likelihood'}, 
        one_sided_lower=True
    )
    ax.set_xlim([-600,0])
    ax.get_figure().savefig('./output/likelihood_test_pycsep.pdf')

    ax = plots.plot_poisson_consistency_test(
        evaluation_results['s-test'], 
        plot_args={'xlabel': 'log-likelihood'}, 
        one_sided_lower=True
    )
    ax.set_xlim([-220, -100])
    ax.get_figure().savefig('./output/spatial_test_pycsep.pdf')

    ax = plots.plot_poisson_consistency_test(
        evaluation_results['m-test'], 
        plot_args={'xlabel': 'log-likelihood'}, 
        one_sided_lower=True
    )
    ax.set_xlim([-35, -10])
    ax.get_figure().savefig('./output/magnitude_test_pycsep.pdf')
