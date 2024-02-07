import pandas as pd
import numpy as np
import argparse
import itertools

import re
import os
from os import path
import sys
import time

# Linux dvfs policies: https://www.kernel.org/doc/Documentation/cpu-freq/governors.txt
policies = ["ondemand", "conservative", "performance", "schedutil", "powersave"]

# total time to run for, in ms
times = [300000, 600000]

# diff flink rates
rates = [100000, 200000, 300000, 400000]

# number of mappers
mappers = [4, 8, 12, 16]

# not exploring different combo for these yet
itrs = [1]
dvfss = [1]
sources = [16, 20] # num of sources
sinks = [16, 20] # num of sinks
ncores = [16, 20] # num of physical cores to use

df_dict = {
    'i': [], 'itr': [], 'dvfs': [], 'rate': [], 'policy': [], 'nmappers':[],
    'watts_avg': [], 'watts_std': [],
    
    'pollCnt': [], 'c1Cnt': [], 'c1eCnt': [],'c3Cnt': [], 'c6Cnt': [], 
    'rxPackets': [], 'rxBytes': [], 'txPackets': [], 'txBytes': [],
    'erxPackets': [], 'erxBytes':[], 'etxPackets': [], 'etxBytes':[],
    
    'SinknumRecordsInPerSecond_avg': [], 'SinknumRecordsInPerSecond_std': [], 
    'SinknumRecordsOutPerSecond_avg': [], 'SinknumRecordsOutPerSecond_std': [], 
    'SinkbusyTimeMsPerSecond_avg': [], 'SinkbusyTimeMsPerSecond_std': [], 
    'SinkbackPressuredTimeMsPerSecond_avg': [], 'SinkbackPressuredTimeMsPerSecond_std': [], 
    'SinkbusyTime_%': [], 'SinkbackPressuredTime_%': [], 

    'SourcenumRecordsInPerSecond_avg': [], 'SourcenumRecordsInPerSecond_std': [], 
    'SourcenumRecordsOutPerSecond_avg': [], 'SourcenumRecordsOutPerSecond_std': [], 
    'SourcebusyTimeMsPerSecond_avg': [], 'SourcebusyTimeMsPerSecond_std': [], 
    'SourcebackPressuredTimeMsPerSecond_avg': [], 'SourcebackPressuredTimeMsPerSecond_std': [], 
    'SourcebusyTime_%': [], 'SourcebackPressuredTime_%': [], 

    'MappernumRecordsInPerSecond_avg': [], 
    'MappernumRecordsInPerSecond_std': [], 'MappernumRecordsOutPerSecond_avg': [], 
    'MappernumRecordsOutPerSecond_std': [], 'MapperbusyTimeMsPerSecond_avg': [], 
    'MapperbusyTimeMsPerSecond_std': [], 'MapperbackPressuredTimeMsPerSecond_avg': [], 
    'MapperbackPressuredTimeMsPerSecond_std': [],
    'MapperbusyTime_%': [], 'MapperbackPressuredTime_%': []
}

#print(df_dict)
print("*****************************************************************")

def resetdf():
    global df_dict
    df_dict = {
    'i': [], 'itr': [], 'dvfs': [], 'rate': [], 'policy': [], 'nmappers':[],
    'watts_avg': [], 'watts_std': [],
        
    'pollCnt': [], 'c1Cnt': [], 'c1eCnt': [],'c3Cnt': [], 'c6Cnt': [], 
    'rxPackets': [], 'rxBytes': [], 'txPackets': [], 'txBytes': [],
    'erxPackets': [], 'erxBytes':[], 'etxPackets': [], 'etxBytes':[],
    
    'SinknumRecordsInPerSecond_avg': [], 'SinknumRecordsInPerSecond_std': [], 
    'SinknumRecordsOutPerSecond_avg': [], 'SinknumRecordsOutPerSecond_std': [], 
    'SinkbusyTimeMsPerSecond_avg': [], 'SinkbusyTimeMsPerSecond_std': [], 
    'SinkbackPressuredTimeMsPerSecond_avg': [], 'SinkbackPressuredTimeMsPerSecond_std': [], 
    'SinkbusyTime_%': [], 'SinkbackPressuredTime_%': [], 

    'SourcenumRecordsInPerSecond_avg': [], 'SourcenumRecordsInPerSecond_std': [], 
    'SourcenumRecordsOutPerSecond_avg': [], 'SourcenumRecordsOutPerSecond_std': [], 
    'SourcebusyTimeMsPerSecond_avg': [], 'SourcebusyTimeMsPerSecond_std': [], 
    'SourcebackPressuredTimeMsPerSecond_avg': [], 'SourcebackPressuredTimeMsPerSecond_std': [], 
    'SourcebusyTime_%': [], 'SourcebackPressuredTime_%': [], 

    'MappernumRecordsInPerSecond_avg': [], 
    'MappernumRecordsInPerSecond_std': [], 'MappernumRecordsOutPerSecond_avg': [], 
    'MappernumRecordsOutPerSecond_std': [], 'MapperbusyTimeMsPerSecond_avg': [], 
    'MapperbusyTimeMsPerSecond_std': [], 'MapperbackPressuredTimeMsPerSecond_avg': [], 
    'MapperbackPressuredTimeMsPerSecond_std': [],
    'MapperbusyTime_%': [], 'MapperbackPressuredTime_%': []
    }
    
def parseFile(loc, rate, itr, dvfs, policy, i, mapper, timems):
    file=f"{loc}/summary.csv"
    
    df_dict['i'].append(i)
    df_dict['itr'].append(itr)
    df_dict['nmappers'].append(mapper)
    
    df_dict['dvfs'].append(dvfs)
    
    df_dict['policy'].append(policy)
    df_dict['rate'].append(rate)
        
    df = pd.read_csv(file)
    df = df[df.columns.drop(list(df.filter(regex='Cnt')))]
    df = df[df.columns.drop(list(df.filter(regex='Bytes')))]
    
    dff = df[df['name'].str.contains('Sink')]
    dff.columns = 'Sink' + dff.columns
    cols = dff.columns
    for col in cols[2:]:
        df_dict[col].append(dff.mean(numeric_only=True)[col])

    dff = df[df['name'].str.contains('Source')]
    dff.columns = 'Source' + dff.columns
    cols = dff.columns
    for col in cols[2:]:
        df_dict[col].append(dff.mean(numeric_only=True)[col])

    dff = df[df['name'].str.contains('Mapper')]
    dff.columns = 'Mapper' + dff.columns
    cols = dff.columns
    for col in cols[2:]:
        df_dict[col].append(dff.mean(numeric_only=True)[col])

    # server2_rapl.log collects Power (energy/second) data
    jfile = f"{loc}/server2_rapl.log"
    with open(jfile) as file:
        lines = [float(line.rstrip()) for line in file]

        # extract values from 40%-80% of total time to account for warmup time and capture region of compute
        time_in_secs = timems/1000
        stime = int(time_in_secs * 0.4)
        etime = int(time_in_secs * 0.8)

        # get the average Power within this timeslot
        df_dict['watts_avg'].append(float(round(np.mean(lines[stime:etime]), 2)))
        df_dict['watts_std'].append(float(round(np.std(lines[stime:etime]), 2)))

    # stats.csv is collected from Flink on a 10 sec basis
    jfile = f"{loc}/stats.csv"
    with open(jfile) as file:
        poll = []
        c1 = []
        c1e = []
        c3 = []
        c6 = []
        rxp = []
        rxb = []
        txp = []
        txb = []
        erxp = []
        erxb = []
        etxp = []
        etxb = []
        for line in file:
            ll = [int(a) for a in line.strip().split(',')]
            poll.append(ll[0])
            c1.append(ll[1])
            c1e.append(ll[2])
            c3.append(ll[3])
            c6.append(ll[4])
            rxp.append(ll[5])
            rxb.append(ll[6])
            txp.append(ll[7])
            txb.append(ll[8])
            erxp.append(ll[9])
            erxb.append(ll[10])
            etxp.append(ll[11])
            etxb.append(ll[12])

        # extract values from 40%-80% of total time to account for warmup time and capture region of compute
        time_in_secs = timems/1000
        stime = int(time_in_secs * 0.4)
        etime = int(time_in_secs * 0.8)

        # convert it to 10 seconds basis
        ss = int(stime/10)
        ee = int(etime/10)
        
        df_dict['pollCnt'].append(np.sum(poll[ss:ee]))
        df_dict['c1Cnt'].append(np.sum(c1[ss:ee]))
        df_dict['c1eCnt'].append(np.sum(c1e[ss:ee]))
        df_dict['c3Cnt'].append(np.sum(c3[ss:ee]))
        df_dict['c6Cnt'].append(np.sum(c6[ss:ee]))
        df_dict['rxPackets'].append(np.sum(rxp[ss:ee]))
        df_dict['rxBytes'].append(np.sum(rxb[ss:ee]))        
        df_dict['txPackets'].append(np.sum(txp[ss:ee]))
        df_dict['txBytes'].append(np.sum(txb[ss:ee]))
        df_dict['erxPackets'].append(np.sum(erxp[ss:ee]))
        df_dict['erxBytes'].append(np.sum(erxb[ss:ee]))
        df_dict['etxPackets'].append(np.sum(etxb[ss:ee]))
        df_dict['etxBytes'].append(np.sum(etxb[ss:ee]))

def parse(loc1, name):    
    nrepeat = 10
    resetdf()
    #print(df_dict)

    # Generate combinations of items from the 
    combinations = list(itertools.product(policies, rates, times, itrs, dvfss, mappers, ncores, sources, sinks))
    
    # Print the combinations
    for combo in combinations:
        policy, rate, timems, itr, dvfs, mapper, cores, source, sink = combo
        
        for i in range(nrepeat):                            
            loc=f"{loc1}/{name}_cores{cores}_frate{rate}_{timems}_fbuff-1_itr{itr}_{policy}dvfs{dvfs}_source{source}_mapper{mapper}_sink{sink}_repeat{i}"
            if not path.exists(loc+ "/summary.csv"):
                break
            print(loc)
            parseFile(loc, rate, itr, dvfs, policy, i, mapper, timems)
            
    #print(df_dict)
    dd1 = pd.DataFrame(df_dict)
    print(len(dd1.index))    
    dd1.to_csv(f"{loc1}/combined.csv", mode='w')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", help="log location", required=True)
    parser.add_argument("--name", help="ie query1", default="query1", required=True)
    args = parser.parse_args()
    
    loc=args.log
    name=args.name
    
    try:        
        parse(loc, name)
    except Exception as error:
        print(error)
        
