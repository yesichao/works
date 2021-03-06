import warnings
import wfdb
import os
import numpy as np
import operator
from utils import *
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
warnings.filterwarnings("ignore")
data_path='D:/python/bwl res_net/MIT-BIH'
DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
data = {'train': DS1,
        'test': DS2
        }
target_class = ['train', 'test']
MITBIH_classes = ['N', 'L', 'R', 'e', 'j', 'A', 'a', 'J', 'S', 'V', 'E', 'F']
def check_overtime(i,length):
    s = data[target_class[i]]
    N_sig = []
    S_sig = []
    V_sig = []
    F_sig = []
    over_time = np.zeros(4)
    for k in range(len(s)):
        start_time = 0
        end_time = start_time + length
        print(data_path + '/' + str(s[k]) + target_class[i])
        record = wfdb.rdrecord(data_path + '/' + str(s[k]), sampfrom=0, channel_names=['MLII'])
        sigal = record.p_signal
        annotation = wfdb.rdann(data_path + '/' + str(s[k]), 'atr')
        while end_time <= sigal.shape[0]:
            sign = sigal[start_time:end_time]
            seg_class = []
            for j in range(annotation.ann_len - 1):
                if annotation.sample[j] >= start_time and annotation.sample[j] <= end_time:
                    if annotation.symbol[j] == 'N' or annotation.symbol[j] == 'L' or annotation.symbol[j] == 'R' or \
                            annotation.symbol[j] == 'e' or annotation.symbol[j] == 'j':
                        seg_class.append(0)
                    elif annotation.symbol[j] == 'A' or annotation.symbol[j] == 'a' or annotation.symbol[j] == 'J' or \
                            annotation.symbol[j] == 'S':
                        seg_class.append(1)
                    elif annotation.symbol[j] == 'V' or annotation.symbol[j] == 'E':
                        seg_class.append(2)
                    elif annotation.symbol[j] == 'F':
                        seg_class.append(3)
            if len(set(seg_class)) == 1 and seg_class[0] == 0:
                N_sig.append(sign)
            elif len(set(seg_class)) != 0:
                while 0 in seg_class:
                    seg_class.remove(0)
                if max(seg_class, key=seg_class.count) == 1:
                    S_sig.append(sign)
                elif max(seg_class, key=seg_class.count) == 2:
                    V_sig.append(sign)
                elif max(seg_class, key=seg_class.count) == 3:
                    F_sig.append(sign)
            start_time = end_time
            end_time = start_time + length
    num = [len(N_sig), len(S_sig), len(V_sig), len(F_sig)]
    baseline = max(num)
    for nums in range(len(num)):
        over_time[nums] =round(length * (1 - num[nums] / baseline))
    print(over_time,num)
    return over_time