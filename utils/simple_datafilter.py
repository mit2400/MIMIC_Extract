import pandas as pd
import h5py

def filter_by_hour(df,max_hours):
    hours_in = df.index.get_level_values(3)
    condition = hours_in <= max_hours # 10days
    df=df[condition]
    return df

def concat_h5(file1,file2,keys,max_hours,target):
    for key in keys:
        df1 = pd.read_hdf(file1,key)
        df2 = pd.read_hdf(file2,key)

        if key=='vitals_labs' or key == 'vitals_labs_mean':
            df1=filter_by_hour(df1,max_hours)
            df2=filter_by_hour(df2,max_hours)

        if key =='patients':
            df1.append(df2).to_hdf(target,key,format='table')
        else:
            df1.append(df2).to_hdf(target,key)

