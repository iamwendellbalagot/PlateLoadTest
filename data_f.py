import pandas as pd
import numpy as np
import sqlite3

def create_df():
    in1 = np.linspace(19.27, 19.35, 60)
    in2 = np.linspace(19.35, 19.51, 240)
    in3 = np.linspace(19.51, 19.98, 600)
    in4 = np.linspace(19.98, 21.24, 1200)
    in5 = np.linspace(21.24, 24.62, 2400)


    in1_ = np.linspace(19.27 + 0.12, 19.35+ 0.12, 60)
    in2_ = np.linspace(19.35+ 0.12, 19.51+ 0.12, 240)
    in3_ = np.linspace(19.51+ 0.12, 19.98+ 0.12, 600)
    in4_ = np.linspace(19.98+ 0.12, 21.24+ 0.12, 1200)
    in5_ = np.linspace(21.24+ 0.12, 24.62+ 0.12, 2400)
    
    

    s1 = np.concatenate([in1,in2, in3, in4, in5])
    s2 = np.concatenate([in1_,in2_, in3_, in4_, in5_])
    
    increments = [in1,in2, in3, in4, in5]

    df = pd.DataFrame()
    df['S1'] = s1
    df['S2'] = s2

    load = []
    increment = []
    time_per_test = []
    for c,inc in enumerate([1,2,3,4,5]):
        len_per_inc = len(increments[c])
        for i in range(len_per_inc):
            increment.append(inc)
    for c,lo in enumerate([50,75,100,125,150]):
        len_per_inc = len(increments[c])
        print(len_per_inc)
        for i in np.random.normal(lo, 0.4,len_per_inc):
            load.append(i)
            time_per_test.append(len_per_inc / 60)
    df['S3'] = load
    df['INCREMENT'] = increment
    df['PRESSURE'] = df['S3'] / 0.09
    df['INITIAL_SET1'] = 19.27
    df['INITIAL_SET2'] = 19.40
    df['PLATE_AREA'] = 0.09
    df['WIDTH_PLATE'] = 0.3
    df['WIDTH_FOOTING'] = 1.5
    df['FOS'] = 2.5
    df['TIME_OF_TEST'] = time_per_test
    
    df = df.round(2)
    return df
    
def push_to_sql():
    cnx = sqlite3.connect('./databases/serverdb.db')
    data = create_df()
    data.to_sql(name='OCT4_TEST', con=cnx)

if __name__ == '__main__':
    push_to_sql()