#%% Imports

import pandas as pd
import matplotlib
#import pickle5 as pickle
from matplotlib import pyplot as plt
import os
from glob import glob

import numpy as np

# %%
N_COLORS = 30
viridis = matplotlib.cm.get_cmap('viridis', N_COLORS)
cls = np.array(viridis.colors[:,:3]*255).astype(int)
cs = ["#{:02x}{:02x}{:02x}".format(r,g,b) for r,g,b in cls]

def find_subs(strs):
    
    ms = list()
    
    for s in strs:
        
        if s[-2] == '_' and s[-1].isdigit():
            ms.append(s[:-2])
        else:
            ms.append(s)
            
    return ms

#%%

class InspectTrain():
    def __init__(self, data_identifier_source, results_dir="../results/", extension=".csv"):
        self.results_dir = results_dir
        self.source = data_identifier_source
        self.extension = extension
        self.train_dir = os.path.join(results_dir, data_identifier_source + '/train/')
        self.data, self.metrics = self.read_data()
        self.runs = list(self.data.keys())
        
    def read_data(self):
        
        dfs = dict()
        cols = list()
        
        for root, _, files in os.walk(self.train_dir):
            for f in files:
                if f.endswith(self.extension):
                    path2csv = os.path.join(root, f)
                    run_name = path2csv.split('/')[-2]
                    df = pd.read_csv(path2csv) # must be changed for other exts
                    dfs[str(run_name)] = df
                    cols = cols + list(df.columns)
                    
        cols = list(set(cols))
        
        for col in cols:
            if 'unnamed' in col.lower():
                cols.remove(col)
                for key in dfs.keys():
                    df = dfs[key]
                    if col in df.columns:
                        df.drop(col, inplace=True, axis=1)
                        dfs[key] = df
                    
        return dfs, cols
    
    def show(self, param, subparam=None, xlabel='epoch', show_stats=False):
        
        if subparam is not None:
            if not isinstance(subparam, list):
                subparam = [subparam]  
        
        plot_dict = dict()
        
        if param in self.metrics:
            if subparam is None:
                subparam = self.runs
            for run in subparam:
                df = self.data[run]
                if param in df.columns:
                    plot_dict[run] = df[param]
            
        elif param in self.runs:
            df = self.data[param]
            if subparam is None:
                subparam = df.columns
            for metric in subparam:
                plot_dict[metric] = df[metric]    
            
        else:
            print('No such run or metric name \'%s\' has been found!'.format(param))
            return -1
        
        fig, ax = plt.subplots(1)
            
        q = 0
        #cs = list(matplotlib.colors.TABLEAU_COLORS.values())
        for key in plot_dict.keys():
            
            if show_stats and (key != 'save'):
                min_val = np.min(plot_dict[key])
                max_val = np.max(plot_dict[key])
                std_val = np.std(plot_dict[key])
                avg_val = np.mean(plot_dict[key])
                med_val = np.median(plot_dict[key])
                print(key, ':', '{:.5f} | '.format(med_val),
                      '{:.5f} +/- {:.5f}'.format(avg_val, std_val),
                      '({:.5f}-{:.5f})'.format(min_val, max_val))
            
            if key == 'save' or param =='save':
                x = np.where(plot_dict[key] > 0)
                ax.vlines(x, 0.4, 0.6, label=key, alpha=0.9, colors=cs[q])
            else:
                ax.plot(plot_dict[key], label=key, alpha=0.6, c=cs[q])
            q += 1
            
        ax.set_xlabel(xlabel)
        ax.set_title((self.source + ': ' + param))
        ax.legend()
            
        return plot_dict
    
    def __getitem__(self, idx):
        
        if isinstance(idx, int):
            key = self.data.keys()[idx]
        elif isinstance(idx, str):
            key = idx
        else:
            return -1
            
        return self.data[key]
    
#%% 

class InspectTest():
    
    def __init__(self, data_identifier_source, results_dir="../results/", extension=".txt"):
        self.data_source = data_identifier_source
        self.test_dir = os.path.join(results_dir, data_identifier_source + '/test/')
        self.extension = extension
        self.scores = self.read_scores()
        self.summary = self.summarize()
        
    def read_scores(self):
        
        scores = dict()
        paths = glob(self.test_dir + '/*/*'+ self.extension)
        paths = sorted(paths, key=str.lower)
        
        for path in paths:
            run_name = path.split('/')[-2]
            df = pd.read_csv(path, sep="\t", header=None)
            scores_array = np.array(df[1])
            if list(df[0])[-1].lower() == 'average':
                scores_array = scores_array[:-1]
            
            scores[str(run_name)] = scores_array
        
        scores = pd.DataFrame.from_dict(scores).T
        
        return scores

    def summarize(self):
        
        dictData = dict()
        
        for s in self.scores.index.values:
            
            data = list(self.scores.loc[s,:])
            
            if s[-2] == '_' and s[-1].isdigit():
                ms = s[:-2]
            else:
                ms = s
                
            if ms in dictData.keys():
                for d in data:
                    dictData[ms].append(d)
            else:
                dictData[ms] = data
        
        try:
            summary = pd.DataFrame.from_dict(dictData).describe().T
        except Exception:
            sumDict = dict()
            for key in dictData.keys():
                rd = dictData[key]
                sumDict[key] = [np.mean(rd), np.std(rd), 
                                np.max(rd), np.min(rd), len(rd)]
                
            summary = pd.DataFrame.from_dict(sumDict).T
            summary.columns = ['mean', 'std', 'max', 'min', 'count']

        return summary
    
    def show(self, incs=None):
        
        df = pd.DataFrame.copy(self.summary)
        
        if incs is not None:
            if not isinstance(incs, list):
                incs = [incs]
            
            filt = np.ones(len(df), dtype=bool)
            
            for inc in incs:
                if inc[0] == '~':
                    filt0 = [inc[1:] not in value for value in df.index.values]
                else:
                    filt0 = [inc in value for value in df.index.values]
            
                filt = np.logical_and(filt0, filt)
            
            df = df[filt]
        
        n_runs = len(df)
        x_pos = np.array(list(range(n_runs)))
        
        runs = df.index.values
        means = df['mean']
        stds = df['std']
        
        fig, ax = plt.subplots()
        ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.7, ecolor='black', capsize=5)
        ax.set_ylabel('Dice Scores')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(runs, rotation=70, ha='right')
        ax.set_title('Dice Scores for ' + self.data_source)
        ax.yaxis.grid(True)

        # Save the figure and show
        plt.tight_layout()
        plt.show()
        
        return df
        
#%% 

class TrainDuration():
    
    def __init__(self, data_identifier_source, results_dir="../results/"):
        self.data_source = data_identifier_source
        self.train_dir = os.path.join(results_dir, data_identifier_source + '/train/')
        self.data = self.read_data()
        self.summary = self.summarize()

    def read_data(self):
        
        data = dict()
        paths = glob(self.train_dir + '/*/epoch_data.csv')
        paths = sorted(paths, key=str.lower)
        
        for path in paths:
            run_name = path.split('/')[-2]
            path_cfg = '/'.join(path.split('/')[:-1]) + '/cfg.py'

            s = run_name
            
            if s[-2] == '_' and s[-1].isdigit():
                main_run = s[:-2]
            else:
                main_run = s
            
            with open(path_cfg, 'rb') as f:
                lines = f.read().splitlines()
                lines = [line.decode("utf-8") for line in lines]
                duration = float(lines[3].split(' ')[2])

            with open(path, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
            last_epoch = int(last_line.split(',')[0])
            
            n_epochs = last_epoch+1
            
            data[str(run_name)] = [main_run, duration/n_epochs, duration, n_epochs]
        
        data = pd.DataFrame.from_dict(data)
        data = data.T
        
        data.columns = ['run_base', 'epoch_duration', 'duration', 'n_epochs']
        
        data['epoch_duration'] = data['epoch_duration'].astype(float)
        
        return data
    
    def summarize(self):
        
        summary = self.data.groupby('run_base')["epoch_duration"].agg([np.mean, np.std, np.min, np.max])
        return summary

#%%

def diceWriter(data, save_name):

    m = data['mean'].apply(lambda x: f"{x:.3f}")
    s = data['std'].apply(lambda x: f"{x:.3f}"[1:])
    
    res = m.to_frame()
    res['std'] = s
    
    res.to_csv(save_name)
    
#%% 

nci_dur = TrainDuration('nci')
nci_dur.summary
#%%

abide_dur = TrainDuration('abide_caltech')
abide_dur.summary
#%%

acdc_dur = TrainDuration('acdc')
acdc_dur.summary

#%%

nci_test = InspectTest('nci')
print(len(nci_test.summary))
diceWriter(nci_test.summary, 'nci_dice.csv')
nci_test.summary

#%% 

abide_test = InspectTest('abide_caltech')
print(len(abide_test.summary))
diceWriter(abide_test.summary, 'abide_caltech_dice.csv')
abide_test.summary
# %%

acdc_test = InspectTest('acdc')
print(len(acdc_test.summary))
diceWriter(acdc_test.summary, 'acdc_dice.csv')
acdc_test.summary
# %%

