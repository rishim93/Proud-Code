import FunctionsRecordLinkageDNB as inf
import pandas as pd
import os
from zipfile import ZipFile

#from recordlinkage.index import Block
#import recordlinkage

inputfileDIR = "D:\\DuplicateDetection\\InputToPython\\"
outputfileDIR = "D:\\DuplicateDetection\\OutputFromPython\\"
processingDIR = "D:\\DuplicateDetection\\Processing\\"
processingFileDIR = "D:\\DuplicateDetection\\Processing\\files"
archive = "D:\\DuplicateDetection\\Archive"


# Get ZIP files from inputfilesDIR
inputfiles = os.listdir(inputfileDIR)


# Move file from inputfilesDIR to ProcessingDIR
for file in inputfiles:
    os.rename(inputfileDIR+"\\"+file,processingDIR+"\\"+file)


# Pick up files to process from Processing folder
processingfiles = os.listdir(processingDIR)




def processIndividualfiles():
    # Read files one at a time
    for file in os.listdir(processingFileDIR):
        filename = file
        print (filename+"      for loop")
        # Read File
        dffull = pd.read_csv(processingFileDIR+"\\"+filename,sep = '|', encoding = 'utf-8')
    #        dffull = dffull[0:1000]
        #set sourceid = mean of sourceid column
        
        sourceid = 1 #int(dffull['SourceID'].mean())
        FNLiD = int(dffull['FNLiD'].mean())
        # Remove Columns based on source
        dffull = inf.essentialcolumns(dffull,sourceid)
        
        print(filename+"      comparison Started")
        df,cv_full = inf.processing(dffull,sourceid)
        print(filename+"      comparison ended")
        if len(cv_full!=0):
            print(filename+"      cv_full != 0")
            df.reset_index(inplace = True)
            cv_full.reset_index(inplace = True)
            
            counts_cv_full = pd.DataFrame(cv_full.level_0.value_counts())
            counts_cv_full.reset_index(inplace = True)
            
            def getlinks(row):
                return list(cv_full[(cv_full['level_0'] == row)]['level_1'])
            
            counts_cv_full['links'] = counts_cv_full['index'].apply(getlinks)
    
            inf.getlinksoflist(counts_cv_full)
    
            counts_cv_full.apply(inf.concatlists, axis = 1)
    
            inf.nulltoindex(counts_cv_full)
            
            counts_cv_full = counts_cv_full.explode('links')
            
            cols = ['links','linkoflist']
            counts_cv_full = counts_cv_full[cols]
            counts_cv_full = counts_cv_full.astype(int)
            
    
            result = pd.merge(df, counts_cv_full, how='inner', left_on='index', right_on='links',
                              left_index=False, right_index=False)
            result['IDmask1'] = result['IDmask1'].astype(str)
            result['IDmask2'] = result['IDmask2'].astype(str)
            result['links'] = result['links'].astype(str)
            result['linkoflist'] = result['linkoflist'].astype(str)
            result['FNLiD'] = result['FNLiD'].astype(str)
            result['dup'] = result['links']+result['linkoflist']
            result.drop_duplicates(subset ="dup", keep = 'first',inplace = True)
            
            del result['dup']
            
            try:
                del result['level_0']
            except:
                pass
            cv_full['FNLiD'] = FNLiD
            cv_full.to_csv(outputfileDIR+'\\P01_CV_'+filename,sep = '|',encoding ='utf-8', index = False)
            result.to_csv(outputfileDIR+'\\P01_RES_'+filename,sep = '|',encoding ='utf-8', index = False)
            os.remove(processingFileDIR+"\\"+filename)
        else:
            print(filename+" = No matches")
            os.remove(processingFileDIR+"\\"+filename)

def zipfileextract():
    for zipfile in processingfiles:
        if zipfile.endswith('.zip'):
        # Extract ZIP file in Files folder
            with ZipFile(processingDIR+"\\"+zipfile, 'r') as zipObj:
                zipObj.extractall(processingFileDIR)
        else:
            
            pass
        processIndividualfiles()
        
    
        
    # Move Zip to ARCHIVE

        if zipfile.endswith('.zip'):
            os.rename(processingDIR+"\\"+zipfile,archive+"\\"+zipfile)
            
if len(processingfiles)>1:
    zipfileextract()
else:
    processIndividualfiles()


            

    

