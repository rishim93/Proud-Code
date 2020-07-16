from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--window-size=600,600")
driver = webdriver.Chrome(r'C:\Users\MadanR\.wdm\drivers\chromedriver\80.0.3987.16\win32\chromedriver.exe',options=chrome_options)



driver.get("<URL>")

search = driver.find_element_by_id("<ElementID>")

search.click()





import os
import time
from datetime import date

files=[]
a= []
files.clear()
def check():
    files = [f for f in os.listdir(r'C:\Downloads')]
    for f in files:
        if f.endswith('.zip'):
            a.append(f)
    return a
while len(files) ==0:
    files.clear()
    time.sleep(30)
    files = check()
else:
    driver.quit()


today = date.today()
d1 = today.strftime("%Y%m%d")
pathDownloads = r'C:\\Downloads\\'

for filename in files:
    if filename.endswith('.zip'):
        splitname= filename.split('.')
        newname = splitname[0]+str(d1)+'.'+splitname[1]
        os.rename(pathDownloads+filename,pathDownloads+newname)

import shutil
dest = r'Y:\\'
filetomove = [f for f in os.listdir(pathDownloads)]
for f in filetomove:
    if f.endswith('.zip'):
        shutil.move(pathDownloads+f,dest)
        
filestodelete = []
filestodelete = [f for f in os.listdir(pathDownloads)]
for f in filestodelete:
    if f.endswith('.zip'):
        os.remove(f)
