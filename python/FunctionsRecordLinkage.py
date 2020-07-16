from recordlinkage.index import Block
import recordlinkage
import pandas as pd
import numpy as np

def essentialcolumns(df,sourceid):
    if sourceid ==1:
        cols = ['DupID', 'SupplierID', 'IDmask1',
       'IDmask2', 'FileHistoryID',
       'SourceID', 'AddressKey', 'BusinessNameKey', 'TradestyleKey',
       'PostCodeKey','FNLiD']
        
        df = df[cols]
        return df
    


#def intervals(parts, duration,postal_pairs):
#    part_duration = duration // parts
#    return [((i * part_duration)+1, (i + 1) * part_duration) for i in range(parts)]

def processing(df,sourceid):
    if sourceid ==1:
        postal_indexer = Block('PostCodeKey')
        postal_pairs = postal_indexer.index(df)
        for i in [20,40,60,80,100]:
            if (len(postal_pairs)/i) < 1000000:
                intervalparts = i
                break
            else:
                intervalparts = 100
# Get Interval Parts        
        inter = intervals(intervalparts,len(postal_pairs))
        
        comp_postal = recordlinkage.Compare(n_jobs = 20)
        comp_postal.string('BusinessNameKey', 'BusinessNameKey', method='jarowinkler',label = 'BusinesNameCompare')
        comp_postal.string('TradestyleKey', 'BusinessNameKey', method='jarowinkler',label = 'BNTSCompare')
        comp_postal.string('AddressKey', 'AddressKey', method='jarowinkler',label = 'AddressCompare')
        
        cv_full = comp_postal.compute(postal_pairs[0:inter[1]],df)
        cv_full = cv_full[((cv_full.BusinesNameCompare.between(0.95,1,inclusive = True)) | 
                                    (cv_full.BNTSCompare.between(0.95,1,inclusive = True))) &
                             (cv_full.AddressCompare.between(0.95,1,inclusive = True))]
        for i in range(1,len(inter)-1):
            cv = comp_postal.compute(postal_pairs[inter[i]+1:inter[i+1]],df)
            cv = cv[((cv.BusinesNameCompare.between(0.95,1,inclusive = True)) | 
                                    (cv.BNTSCompare.between(0.95,1,inclusive = True))) &
                             (cv.AddressCompare.between(0.95,1,inclusive = True))]
            frames = [cv_full,cv]
            cv_full = pd.concat(frames)
            del cv
       

#        print(df.columns)
#        print(cv_full.columns)
        return df,cv_full
#        return postal_pairs

# calculate intervals
def intervals(parts, duration):
    part_duration = duration // parts
    inter =  [((i * part_duration)+1, (i + 1) * part_duration) for i in range(parts)]
    inter1 = [0]
    for x,y in inter:
        inter1.append(y)
    inter1[parts] = duration
    return inter1


def getlinks(row,df):
    return list(df[(df['level_0'] == row)]['level_1'])


def getlinksoflist(df):
    df.linkoflinks = None 
    c95_list = df.links.tolist()
    m = np.tril([[any(x in l2 for x in l1) for l2 in c95_list] for l1 in c95_list],-1)
    df['linkoflist'] = (df.loc[np.argmax(m, axis=1), 'index']
                                      .where(m.any(1)).to_numpy())

def concatlists(df):
    return df['links'].append(df['index'])

def nulltoindex(df):
    df['linkoflist'] = np.where(df['linkoflist'].isnull(),df['index'],df['linkoflist'])


