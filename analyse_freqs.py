import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from utils import independence_tests
from visualizations import plot_3category_comparison, plot_slang_nonslang_comparison

file_names = {"slang 2020": 'data/frequencies/freq_slang_counts_24h_2020.csv',
              "slang 2010": 'data/frequencies/freq_slang_counts_24h_2010.csv',
              "nonslang 2020": 'data/frequencies/freq_nonslang_counts_24h_2020.csv',
              "nonslang 2010": 'data/frequencies/freq_nonslang_counts_24h_2010.csv',
              "sample 2020": 'data/frequencies/freq_sample_words_24h_2020.csv',
              "sample 2010": 'data/frequencies/freq_sample_words_24h_2010.csv',
              "hybrid 2010": "data/frequencies/freq_hybrid_counts_24h_2010.csv",
              "hybrid 2020": "data/frequencies/freq_hybrid_counts_24h_2020.csv",
              }

def divide_by_larger_freq(X, colname1="freq2020", colname2="freq2010"):
    x,y = X[colname1], X[colname2]
    if x >= y:
        return x/y
    else:
        return y/x

def merge_freq_dfs(freq2010, freq2020, NORMALIZING_CONSTANT=6.4):
    """
    Merge the frequency dataframes of 2010 & 2020, and compute various change statistics
    """
    freq2010.columns = ['freq2010', 'word', 'year', 'type']
    freq2020.columns = ['freq2020', 'word', 'year', 'type']
    all_freqs = pd.merge(freq2010, freq2020[['freq2020', 'word']], on="word", how="inner")
    all_freqs["freq2020_norm"] = all_freqs.freq2020.apply(lambda x: x / NORMALIZING_CONSTANT)

    all_freqs["freq_diff_unnormalized"] = all_freqs.freq2020 / (all_freqs.freq2010)
    all_freqs["freq_diff"] = all_freqs.freq2020_norm / (all_freqs.freq2010)

    all_freqs["div_freq_larger"] = all_freqs[["freq2020_norm", "freq2010"]].apply(
                                      lambda x: divide_by_larger_freq(x, colname1="freq2020_norm"), axis=1)

    # calculates frequency growth
    all_freqs["abs_diff_norm"] = np.abs(all_freqs.freq2020_norm - all_freqs.freq2010)/ (all_freqs.freq2010)

    all_freqs["relative_diff"] = 2*np.abs(all_freqs.freq2020_norm - all_freqs.freq2010)/ \
                                 (all_freqs.freq2020_norm + all_freqs.freq2010)

    all_freqs["log_diff"] = np.log(all_freqs.freq2020_norm/all_freqs.freq2010)
    all_freqs["abs_log_diff"] = all_freqs["log_diff"].apply(lambda x: abs(x))

    return all_freqs

def get_freq_difference_stats(save=True):
    slang2010 = pd.read_csv(file_names["slang 2010"])
    slang2020 = pd.read_csv(file_names["slang 2020"])
    slang_all = merge_freq_dfs(slang2010, slang2020)
    if save: slang_all.to_csv("data/frequencies/slang_all_freqs.csv")

    nonslang2010 = pd.read_csv(file_names["nonslang 2010"])
    nonslang2020 = pd.read_csv(file_names["nonslang 2020"])
    nonslang_all = merge_freq_dfs(nonslang2010, nonslang2020)
    if save: nonslang_all.to_csv("data/frequencies/nonslang_all_freqs.csv")

    hybrid2010 = pd.read_csv(file_names["hybrid 2010"])
    hybrid2020 = pd.read_csv(file_names["hybrid 2020"])
    hybrid_all = merge_freq_dfs(hybrid2010, hybrid2020)
    if save: hybrid_all.to_csv("data/frequencies/hybrid_all_freqs.csv")

    return slang_all, nonslang_all, hybrid_all

def print_slang_nonslang_comparison(s_all, ns_all):
    print("results for log(freq 2020/freq 2010):")
    print_averages_and_medians(s_all=s_all, ns_all=ns_all, curr_col="log_diff")

    print("results for absolute value of log(freq 2020/freq 2010):")
    print_averages_and_medians(s_all=s_all, ns_all=ns_all, curr_col="abs_log_diff")

    print("results for normalized 2020 freqs divided by 2010 freqs:")
    print_averages_and_medians(s_all=s_all, ns_all=ns_all, curr_col="freq_diff")


def print_averages_and_medians(s_all, ns_all, curr_col):
    print("average: slang={}, nonslang={}, \n median: slang={}, nonslang={}".format(
                                                        "%.2f" % np.average(s_all[curr_col]),
                                                        "%.2f" % np.average(ns_all[curr_col]),
                                                        "%.2f" % np.median(s_all[curr_col]),
                                                        "%.2f" % np.median(ns_all[curr_col]),
                                                                        ))

def print_average_frequencies():
    avgs = {}
    for (k,fn) in file_names.items():
        df = pd.read_csv(fn)
        avg_freq = np.average(df.freq.values)
        print("average frequency for", k, "is", avg_freq)
        avgs[k] = avg_freq
    print("the frequency of nonslang words between 2010 and 2020, increased times ",
          avgs["nonslang 2020"]/avgs["nonslang 2010"])
    print("the frequency of slang words between 2010 and 2020, increased times ",
          avgs["slang 2020"]/avgs["slang 2010"])
    print("the frequency of sample words between 2010 and 2020, increased times ",
          avgs["sample 2020"]/avgs["sample 2010"])

print_average_frequencies()
get_freq_difference_stats()

