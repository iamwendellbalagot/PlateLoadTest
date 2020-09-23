import serial
import numpy as np
import sqlite3
import pandas as pd
from tqdm import tqdm
import plotly.express as px
import plotly.graph_objects as go

from createtable import create_table


class GetData:
    def __init__(self, path='./databases/serverdb.db'):
        try:
            self.conn = sqlite3.connect(path)
            self.c = self.conn.cursor()
            
        except:
            print('Device not found.')
        
    
    def get_dataframe(self, table='sensors_data', path='./databases/serverdb.db'):
        conn = sqlite3.connect(path)
        df = pd.read_sql('SELECT * FROM {}'.format(table), con=conn)
        conn.close()
        return df
        
    def upload_data(self, port='', baud=9600, n=10,
                        table = 'table',
                        inc = 'none',
                        path='./databases/serverdb.db'):
                        
        arduino = serial.Serial(port, baud)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        readings = []
        for i in tqdm(range(n)):
            data = arduino.readline()[:-2].decode('utf-8')
            data = [float(i) for i in data.split('\t')]
            data.append(inc)
            readings.append(data)
            
            c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?);',tuple(data));
            conn.commit()
        conn.close()
        
    def generate_df(self, port='', baud=9600, n=10):
        arduino = serial.Serial(port, baud)
        readings = []
        for i in tqdm(range(n)):
            data = arduino.readline()[:-2].decode('utf-8')
            data = [float(i) for i in data.split('\t')]
            readings.append(data)
        df = pd.DataFrame(readings, columns=['S1', 'S2', 'S3'])
        return df
        
    def upload_generate(self, port='', baud=9600, n=10,
                        table = 'table',
                        inc = 0,
                        area = 0,
                        set1 =0,
                        set2=0,
                        w_plate = 0,
                        w_footing = 0,
                        fs = 1,
                        path='./databases/serverdb.db'):
        arduino = serial.Serial(port, baud)
        try:
            conn = sqlite3.connect(path)
            c = conn.cursor()
            readings = []
            
            for i in tqdm(range(n)):
                data = arduino.readline()[:-2].decode('utf-8')
                data = [float(i) for i in data.split('\t')]
                data.append(inc)
                data.append(round(data[2]/ area,1))
                data.append(set1)
                data.append(set2)
                data.append(area)
                data.append(w_plate)
                data.append(w_footing)
                data.append(fs)
                data.append(n)
                readings.append(data)
                
                c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?,?,?,?);',tuple(data));
                conn.commit()
            print('FFF')
            df = pd.DataFrame(readings, columns=['S1', 'S2', 'S3', 'INCREMENT', 'PRESSURE', 'SET1', 'SET2',
                                                 'PLATE_AREA', 'WIDTH_PLATE', 'WIDTH_FOOTING', 'FOS', 'TIME'])
            print('DF RETURNED')
            return df
            conn.close()
        except:
            print('DUPP')
            conn.close()
            query = '''CREATE TABLE IF NOT EXISTS {0} (
                                        S1 REAL,
                                        S2 REAL,
                                        S3 REAL,
                                        INCREMENT REAL,
                                        PRESSURE REAL,
                                        INITIAL_SET1 REAL,
                                        INITIAL_SET2 REAL,
                                        PLATE_AREA REAL,
                                        WIDTH_PLATE REAL,
                                        WIDTH_FOOTING REAL,
                                        FOS REAL,
                                        TIME_OF_TEST REAL

                                    );'''.format(table)
            conn = sqlite3.connect(path)
            c = conn.cursor()
            c.execute(query)
            readings = []
            for i in tqdm(range(n)):
                data = arduino.readline()[:-2].decode('utf-8')
                data = [float(i) for i in data.split('\t')]
                data.append(inc)
                data.append(round(data[2]/ area,1))
                data.append(set1)
                data.append(set2)
                data.append(area)
                data.append(w_plate)
                data.append(w_footing)
                data.append(fs)
                data.append(n)
                readings.append(data)
                
                c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?,?,?,?);',tuple(data));
                conn.commit()
            df = pd.DataFrame(readings, columns=['S1', 'S2', 'S3', 'INCREMENT', 'PRESSURE', 'SET1', 'SET2',
                                                 'PLATE_AREA', 'WIDTH_PLATE', 'WIDTH_FOOTING', 'FOS', 'TIME'])
            print('DF2 RETURNED')
            return df
            conn.close()
        

    def get_ubc(self,df):
        df['lag'] = df.S.diff()
        idx = df[df.lag ==df.lag.max()].index[0] -1
        ubc = df.iloc[idx]['P']
        ubc_set = df.iloc[idx]['S']
        return ubc, ubc_set, idx
    
    
    def get_PS(self,df):
        summmary_df = pd.DataFrame(columns = ['P', 'S1', 'S2', 'S1_S2'])
        df['diff1'] = (df.S1.values - df.INITIAL_SET1.values) * 10
        df['diff2'] = (df.S2.values - df.INITIAL_SET2.values) * 10

        unik = df.INCREMENT.unique()
        set1_per_inc = []
        set2_per_inc = []
        for increment in unik:
            set1_per_inc.append(df[df['INCREMENT']==increment]['diff1'].iloc[-1])
            set2_per_inc.append(df[df['INCREMENT']==increment]['diff2'].iloc[-1])

        summmary_df['S1'] = np.array(set1_per_inc)
        summmary_df['S2'] = np.array(set2_per_inc)
        summmary_df['S1_S2'] = np.array(summmary_df.S1 + summmary_df.S2)
        summmary_df = summmary_df.sort_values('S1_S2') 
        summmary_df['P'] = np.sort(df.groupby('INCREMENT').mean()['PRESSURE'].values)
        
        summmary_df['S'] = np.sort((summmary_df.S1.values + summmary_df.S2.values) / 2)
        summmary_df['TS'] = summmary_df['S'].cumsum()
        return summmary_df.reset_index()
