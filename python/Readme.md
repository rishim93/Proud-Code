### 1. DuplicateDetection.py
  This is the extended version of DuplicateDetection in sql, the files are sent to program in python using SSIS and Processed to match duplicates using record linkage library and   then inhouse code to consolidate all the records to e ingetsed back into SQL server

### 2. FunctionsRecordLinkage.py
  This are all the functions used in DuplicateDetetction.py to work
  
### 3. automatedFilegetter.py
  This program uses selenum to download a zip file and send it to a differnet folder for processing, it also does some basic checks not to overwrite a preexisting file.
    
### 4. API_UI.py
  This was an effort to make a UI based search tool using Differnet APIs and search for the businesses, this is only using google API, other APIs can be added.
