import pandas as pd
import numpy as np
import argparse
#import matplotlib.pylab as plt

import re
import os
from os import path
import sys
import time

LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']

#2600000
#TIME_CONVERSION_khz = 1./(2899999*1000
TIME_CONVERSION_khz = 1./(2600000*1000)
JOULE_CONVERSION = 0.00001526

dvfs_list = ['0c00', '0d00', '0e00', 
             '0f00', '1000', '1100', '1200', 
             '1300', '1400', '1500', '1600', '1700', '1800', '1900', '1a00']
dvfs_dict = {
    "0x0c00" :  1.2,
    "0x0d00" :  1.3,
    "0x0e00" :  1.4,
    "0x0f00" :  1.5,
    "0x1000" : 1.6,
    "0x1100" : 1.7,
    "0x1200" : 1.8,
    "0x1300" : 1.9,
    "0x1400" : 2.0,
    "0x1500" : 2.1,
    "0x1600" : 2.2,
    "0x1700" : 2.3,
    "0x1800" : 2.4,
    "0x1900" : 2.5,
    "0x1a00" : 2.6,
    "0x1b00" : 2.7,
    "0x1c00" : 2.8,
    "0x1d00" : 2.9,
}

df_dict = {
    'i': [], 'itr': [], 'dvfs': [], 'rate': [], 'policy': [], 'watts_avg': [], 'watts_std': [], 
    
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
    'i': [], 'itr': [], 'dvfs': [], 'rate': [], 'policy': [],
    
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
    
def parseFile(loc, rate, itr, dvfs, policy, i):
    file=f"{loc}/summary.csv"
    #print(file)
    df_dict['i'].append(i)
    df_dict['itr'].append(itr)
    #if '0x'+dvfs in dvfs_dict:
    #    df_dict['dvfs'].append(dvfs_dict['0x'+dvfs])
    df_dict['dvfs'].append(dvfs)
        
    #df_dict['dvfs'].append(dvfs)
    df_dict['policy'].append(policy)
    df_dict['rate'].append(rate)
        
    df = pd.read_csv(file)
    df = df[df.columns.drop(list(df.filter(regex='Cnt')))]
    df = df[df.columns.drop(list(df.filter(regex='Bytes')))]
    #print(df)
    
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

    #jfile = f"{loc}/server2_rapl.log"
    #with open(jfile) as file:
    #    lines = [float(line.rstrip()) for line in file]
    #    print(len(lines))
    #    df_dict['watts_avg'].append(float(round(np.mean(lines[300:600]), 2)))
    #    df_dict['watts_std'].append(float(round(np.std(lines[300:600]), 2)))
        #print(np.std(lines[300:500]))
        
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
        ss = 30
        ee = 60
        df_dict['pollCnt'].append(np.sum(poll[ss:ee]))
        df_dict['c1Cnt'].append(np.sum(c1[ss:ee]))
        df_dict['c1eCnt'].append(np.sum(c1e[ss:ee]))
        df_dict['c3Cnt'].append(np.sum(c3[ss:ee]))
        df_dict['c6Cnt'].append(np.sum(c6[ss:ee]))
        #'rxPackets': [], 'rxBytes': [], 'txPackets': [], 'txBytes': [],
        df_dict['rxPackets'].append(np.sum(rxp[ss:ee]))
        df_dict['rxBytes'].append(np.sum(rxb[ss:ee]))        
        df_dict['txPackets'].append(np.sum(txp[ss:ee]))
        df_dict['txBytes'].append(np.sum(txb[ss:ee]))
        df_dict['erxPackets'].append(np.sum(erxp[ss:ee]))
        df_dict['erxBytes'].append(np.sum(erxb[ss:ee]))
        #print(np.mean(erxb[30:50]), np.std(erxb[30:50]))
        df_dict['etxPackets'].append(np.sum(etxb[ss:ee]))
        df_dict['etxBytes'].append(np.sum(etxb[ss:ee]))

df_dict2 = {
    'i': [], 'itr': [], 'dvfs': [], 'rate': [], 'policy': [], 'joules': [],    
    'rxDescIntLog': [], 'rxBytesIntLog': [], 'txDescIntLog': [], 'txBytesIntLog': [],
    'instructions': [], 'cycles': [], 
    'ref_cycles': [], 'llc_miss': [], 
    'num_interrupts': [], 'time': []
}


def parse(loc1):
    mqps = 0
    cqps = 0
    tins = 0
    tcyc = 0
    trefcyc = 0
    tllcm = 0
    tc3 = 0
    tc6 = 0
    tc7 = 0
    tc1 = 0
    tc1e = 0
    trx_desc = 0
    trx_bytes = 0
    ttx_desc = 0
    ttx_bytes = 0
    tjoules = 0.0
    tnum_interrupts = 0
    ttimestamp = 0
    #loc1="/home/handong/flink/10_12_2023_5.15.89_itrlog"
        
    nrepeat = 4
    resetdf()
    print(df_dict)
    policies = ["ondemand", "conservative","performance", "schedutil", "powersave"]
    for rate in [300000]:
        for policy in policies:
            itr=1
            dvfs=1
            for i in range(nrepeat):
                loc=f"{loc1}/query1_cores16_frate{rate}_600000_fbuff-1_itr{itr}_{policy}dvfs{dvfs}_repeat{i}/"
                print(f"parsing {loc}")
                parseFile(loc, rate, itr, dvfs, policy, i)
            
                mqps = 0
                cqps = 0
                tins = 0
                tcyc = 0
                trefcyc = 0
                tllcm = 0
                tc3 = 0
                tc6 = 0
                tc7 = 0
                tc1 = 0
                tc1e = 0
                trx_desc = 0
                trx_bytes = 0
                ttx_desc = 0
                ttx_bytes = 0
                tjoules = 0.0
                tnum_interrupts = 0
                ttimestamp = 0
            
                for core in range(0, 16):
                    fname=f"{loc}/ITRlogs/linux.flink.dmesg._{core}_{i}"
                    df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
                    df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)].copy()
                    df_non0j['timestamp'] = df_non0j['timestamp'] - df_non0j['timestamp'].min()
                    df_non0j['timestamp'] = df_non0j['timestamp'] * TIME_CONVERSION_khz
                    df_non0j['ref_cycles'] = df_non0j['ref_cycles'] * TIME_CONVERSION_khz
                    df_non0j['joules'] = df_non0j['joules'] * JOULE_CONVERSION
                    df_non0j = df_non0j[(df_non0j['timestamp'] > 300) & (df_non0j['timestamp'] < 600)]
                    
                    tmp = df_non0j[['instructions', 'cycles', 'ref_cycles', 'llc_miss', 'joules', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7','timestamp']].diff()
                    tmp.columns = [f'{c}_diff' for c in tmp.columns]
                    df_non0j = pd.concat([df_non0j, tmp], axis=1)
                    df_non0j.dropna(inplace=True)
                    df.dropna(inplace=True)
                    df_non0j = df_non0j[df_non0j['joules_diff'] > 0]
                    
                    cjoules = df_non0j['joules_diff'].sum()
                    if core == 0 or core == 1:
                        tjoules += cjoules
                    
                    trx_desc += df_non0j['rx_desc'].sum()
                    trx_bytes += df_non0j['rx_bytes'].sum()
                    ttx_desc += df_non0j['tx_desc'].sum()
                    ttx_bytes += df_non0j['tx_bytes'].sum()

                    tins += df_non0j['instructions_diff'].sum()
                    tcyc += df_non0j['cycles_diff'].sum()
                    trefcyc += df_non0j['ref_cycles_diff'].sum()
                    
                    tllcm += df_non0j['llc_miss_diff'].sum()
                    tc1 += df_non0j['c1_diff'].sum()
                    tc1e += df_non0j['c1e_diff'].sum()
                    tc3 += df_non0j['c3_diff'].sum()
                    tc6 += df_non0j['c6_diff'].sum()
                    tc7 += df_non0j['c7_diff'].sum()
                    tnum_interrupts += df.shape[0]
                    ttimestamp += df_non0j['timestamp_diff'].sum()
                    #print(df_non0j['timestamp_diff'].sum())
                df_dict2['i'].append(i)
                df_dict2['itr'].append(itr)
                df_dict2['dvfs'].append(dvfs)
                df_dict2['policy'].append(policy)
                df_dict2['rate'].append(rate)
                df_dict2['joules'].append(round(tjoules/300.0, 2))
                df_dict2['rxDescIntLog'].append(trx_desc)
                df_dict2['rxBytesIntLog'].append(trx_bytes)
                df_dict2['txDescIntLog'].append(ttx_desc)
                df_dict2['txBytesIntLog'].append(ttx_bytes)
                df_dict2['instructions'].append(tins)
                df_dict2['cycles'].append(tcyc)
                df_dict2['ref_cycles'].append(trefcyc)
                df_dict2['llc_miss'].append(int(tllcm))
                df_dict2['num_interrupts'].append(tnum_interrupts)
                df_dict2['time'].append(ttimestamp)

    dd1 = pd.DataFrame(df_dict)
    dd2 = pd.DataFrame(df_dict2)
    dd3 = dd1.merge(dd2, on=['i', 'itr', 'dvfs', 'rate', 'policy'])
    dd3.to_csv(f"{loc1}/combined_ondemand.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", help="log location", required=True)
    args = parser.parse_args()
    
    loc=args.log
    parse(loc)
