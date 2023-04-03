import argparse
from collections import defaultdict
import json
import os

import pandas as pd
from tqdm import tqdm

fitness_columns_Dataset1_Dataset2 = [
    "log10_K50_t",
    "log10_K50_t_95CI_high",
    "log10_K50_t_95CI_low",
    "log10_K50_t_95CI",
    "fitting_error_t",
    "log10_K50unfolded_t",
    "deltaG_t",
    "deltaG_t_95CI_high",
    "deltaG_t_95CI_low",
    "deltaG_t_95CI",
    "log10_K50_c",
    "log10_K50_c_95CI_high",
    "log10_K50_c_95CI_low",
    "log10_K50_c_95CI",
    "fitting_error_c",
    "log10_K50unfolded_c",
    "deltaG_c",
    "deltaG_c_95CI_high",
    "deltaG_c_95CI_low",
    "deltaG_c_95CI",
    "deltaG",
    "deltaG_95CI_high",
    "deltaG_95CI_low",
    "deltaG_95CI",
]
aa_list = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Process data')
    parser.add_argument('-i', '--input', type=str, default="Processed_K50_dG_datasets/K50_dG_Dataset1_Dataset2.csv", help='Input directory')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output directory')
    parser.add_argument('-fc', '--fitness_column', type=str, default="deltaG", \
                        choices=fitness_columns_Dataset1_Dataset2, \
                        help='Fitness column, choices:{}'.format("\t\n".join(fitness_columns_Dataset1_Dataset2)))

    if args is not None:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    return args

def prepare_all_dict(dataset1, fitness_column):
    WT_name = dataset1.loc[:, "WT_name"].unique()
    
    all_dict = {}
    wt_fitness_dict = {}
    wt_seq_dict = {}
    for wt_name in tqdm(WT_name):
        all_dict[wt_name] = {}
        # print(wt_name)
        wt_name_df = dataset1.loc[dataset1["WT_name"] == wt_name, ["aa_seq", "mut_type", fitness_column]]
        # for those who wt has different deltaG, use the mean value
        wt_fitness = wt_name_df.loc[wt_name_df["mut_type"] == "wt", fitness_column].mean()
        wt_fitness_dict[wt_name] = wt_fitness
        wt_seq_dict[wt_name] = wt_name_df.loc[wt_name_df["mut_type"] == "wt", "aa_seq"].values[0]

        mut_types = wt_name_df.loc[wt_name_df["mut_type"] != "wt", "mut_type"]
        for mut_type in mut_types:
            if len(mut_type.split(":")) > 1:
                continue
            # mut_type_list[-1] should be like A1B
            all_dict[wt_name][mut_type] = wt_name_df.loc[wt_name_df["mut_type"] == mut_type, fitness_column].values.item()
    return all_dict, wt_fitness_dict, wt_seq_dict

def prepare_mut_dict(all_dict, wt_fitness_dict, wt_seq_dict):
    
    mut_dict = {}
    for wt, mutations_dict in tqdm(all_dict.items()):
        # print(wt)
        mut_dict[wt] = defaultdict(list)
        for idx, aa in enumerate(wt_seq_dict[wt]):
            mut_dict[wt][f"{aa}{idx+1}"].append((aa, wt_fitness_dict[wt]))
        # print(mut_dict[wt])
        # break
        for mutation in mutations_dict:
            # {"A1": [("B", value), ("C", value)]}
            if mutation[1:-1].isdigit():
                mut_dict[wt][mutation[:-1]].append((mutation[-1], mutations_dict[mutation]))
            elif mutation.startswith("del"):
                mut_dict[wt][mutation[3:]].append(("del", mutations_dict[mutation]))
            elif mutation.startswith("ins"):
                pass # [TODO] don't know how to deal with this
        
    return mut_dict

def main():
    args = parse_args()
    print(args)
    dataset1 = pd.read_csv(args.input)
    
    all_dict, wt_fitness_dict, wt_seq_dict = prepare_all_dict(dataset1, args.fitness_column)

    mut_dict = prepare_mut_dict(all_dict, wt_fitness_dict, wt_seq_dict)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    for mut in mut_dict:
        json.dump(dict(mut_dict[mut]), open(args.output+f"/{mut}.json", "w"))

if __name__ == "__main__":
    main()
