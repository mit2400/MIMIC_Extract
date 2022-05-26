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

def extract_first_mv_idx(Y):
    Y = Y[['vent']]
    #extract hour per subject that first MV start
    first_mv_idx = (Y['vent']==1).groupby('subject_id').idxmax()
    #g[g['vent']==0].index ==> patients who do not get MV treatment
    g = Y.groupby('subject_id').sum()
    first_mv_idx = first_mv_idx.drop((g[g['vent']==0].index))
    return first_mv_idx

def filter_after_MV(X,first_mv_idx):
    X_filter=X.copy()
    for subject_id in (first_mv_idx.index):
        vent_time = first_mv_idx[subject_id][3]
        X_filter = X_filter.drop(X[(X['subject_id']==subject_id) & (X['hours_in'] >= vent_time)].index)
    return X_filter

def filter_earlyexit(X,Y,static,N):
    X_N = X.reset_index(drop=True).groupby('subject_id').filter(lambda x: (x.hours_in > N).any() )
    SID_list = X_N['subject_id'].reset_index(drop=True).unique()
    Y_N=Y.reset_index()
    Y_N=Y_N[Y_N['subject_id'].isin(SID_list)]
    static_N=static.reset_index()
    static_N=static_N[static_N['subject_id'].isin(SID_list)]
    return X_N, Y_N, static_N





