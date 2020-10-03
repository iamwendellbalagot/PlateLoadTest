import pandas as pd
import numpy as np
import sqlite3

def create_df():
    in1 = np.linspace(18, 18.16, 600)
    in2 = np.linspace(18.16, 18.24, 600)
    in3 = np.linspace(18.24, 18.43, 600)
    in4 = np.linspace(18.43, 18.76, 600)
    in5 = np.linspace(18.76, 19.24, 600)
    in6 = np.linspace(19.24, 20.21, 600)
    in7 = np.linspace(20.21, 22.36, 600)

    in1_ = np.linspace(18+0.2, 18.16+0.2, 600)
    in2_ = np.linspace(18.16+0.2, 18.24+0.2, 600)
    
    in3_ = np.linspace(18.24+0.2, 18.43+0.2, 600)
    in4_ = np.linspace(18.43+0.2, 18.76+0.2, 600)
    
    in5_ = np.linspace(18.76+0.2, 19.24+0.2, 600)
    in6_ = np.linspace(19.24+0.2, 20.21+0.2, 600)
    in7_ = np.linspace(20.21+0.2, 22.36+0.2, 600)
    
    

    s1 = np.concatenate([in1,in2, in3, in4, in5, in6, in7])
    s2 = np.concatenate([in1_,in2_, in3_, in4_, in5_, in6_, in7_])


    df = pd.DataFrame()
    df['S1'] = s1
    df['S2'] = s2

    load = []
    increment = []
    for inc in [1,2,3,4,5,6,7]:
        for i in range(600):
            increment.append(inc)
    for l in [50,75,100,125,150,175,200]:
        for i in np.random.normal(l, 0.1,600):
            load.append(i)
    df['S3'] = load
    df['INCREMENT'] = increment
    df['PRESSURE'] = df['S3'] / 0.16
    df['INITIAL_SET1'] = 18
    df['INITIAL_SET2'] = 18.2
    df['PLATE_AREA'] = 0.16
    df['WIDTH_PLATE'] = 0.4
    df['WIDTH_FOOTING'] = 2
    df['FOS'] = 1.5
    df['TIME_OF_TEST'] = 10
    
    df = df.round(2)
    return df
    
def push_to_sql():
    cnx = sqlite3.connect('./databases/serverdb.db')
    data = create_df()
    data.to_sql(name='sensors_data', con=cnx)

if __name__ == '__main__':
    push_to_sql()