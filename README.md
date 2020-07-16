# Proud-Code
These are some of the problems I worked on, with some over the head unique solutions, I have brief description of each of these code samples below.



## sql

### 1. AddressParser.sql : 
  This is a string parser that has been used to parse out canadian addresses
  
  
### 2. DuplicateDataCleaning.sql :
  This is a data cleaning process that I wrote to find duplicates, this process runs before sending the files for duplicate detection in chunks.
  The code that follows this is in python.
  
### 3. ForLoops.sql : 
  This is a reprentation of running for loops in SQL Server, I know its not always the best practice but sometimes its the way to go.
  
## python

### 1. DuplicateDetection.py
  This is the extended version of DuplicateDetection in sql, the files are sent to program in python using SSIS and Processed to match duplicates using record linkage library and   then inhouse code to consolidate all the records to e ingetsed back into SQL server

### 2. FunctionsRecordLinkage.py
  This are all the functions used in DuplicateDetetction.py to work
  
### 3. automatedFilegetter.py
  This program uses selenum to download a zip file and send it to a differnet folder for processing, it also does some basic checks not to overwrite a preexisting file.
    
### 4. API_UI.py
  This was an effort to make a UI based search tool using Differnet APIs and search for the businesses, this is only using google API, other APIs can be added.
