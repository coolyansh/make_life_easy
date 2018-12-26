#Code written by coolyansh

import urllib, datetime
import requests, bs4, sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#location of file where report is written everytime script executes
file=open("C:\\Users\\rays\\Documents\\Automation Completed Downloads\\log_report.txt","a")
currDateTime=str(datetime.datetime.now())
file.write("\nLog Report "+currDateTime+"\n")
file.write("-----------------------------------------------\n\n")


def isTorrentPresent(name,path):
    flag=False
    for root,dirs,file in os.walk(path):
        for filename in file:
            if filename==name:
                flag=True
                break
    return flag

def isMoviePresent(name,path):
    flag=False
    for i in os.listdir(path):
        if i.lower().find(name.lower())!=-1:
            flag=True
            break
    return flag

def removeFromList(ind):
    c=0
    for i in ind:
        if i==False:
            continue
        c+=1
    if c==0:
        file.write("No movie to remove from watchlist.\n")
        return

    #url of IMDb list for editing    
    url="https://www.imdb.com/list/ls045429726/edit"
    chrome_option = Options()
    #location of Chrome user profile data so that user is already logged in to IMDb when page is opened
    chrome_option.add_argument('user-data-dir=C:/Users/rays/AppData/Local/Google/Chrome/Automation Folder')
    browser = webdriver.Chrome(options=chrome_option)
    browser.maximize_window()
    browser.get(url)
    elem=browser.find_elements_by_class_name("lister-item")
    toDel=[]
    for i in range(0,len(elem)):
        if ind[i]==False:
            continue
        cbox=elem[i].find_elements_by_class_name("element-check")
        cbox[0].send_keys(webdriver.common.keys.Keys.SPACE)
        toDel.append(movies[i])
    
    try:
        delButton=browser.find_element_by_id("delete_items")
        delButton.click()
        confirmButton=browser.find_element_by_css_selector("#delete_items_form > div > input")
        confirmButton.click()
        file.write("Successfully removed following movies from Downloads List.\n")
        for i in toDel:
            file.write("\t"+i+"\n")
    except:
        file.write("Error in loading Edit Page\n")
    browser.quit()

def removeTorrent(ind):
    c=0
    for i in ind:
        if i==False:
            continue
        c+=1
        
    if c==0:
        file.write("No torrent to delete.\n")
        return

    for i in range(0,len(ind)):
        if ind[i]==False:
            continue
        try:
            #location of torrent to remove
            os.remove("C:/Users/rays/Documents/Automation Torrents/"+movies[i]+".torrent")
            file.write("Successfully deleted "+movies[i]+" torrent.\n")
        except:
            file.write("Unable to delete "+movies[i]+" torrent\n")
    


#url of YTS(YIFY) Downloads List IMDb        
url="https://www.imdb.com/list/ls045429726/"
chrome_option = Options()
#location of Chrome user profile data so that user is already logged in to IMDb when page is opened
chrome_option.add_argument('user-data-dir=C:/Users/rays/AppData/Local/Google/Chrome/Automation Folder')
browser = webdriver.Chrome(options=chrome_option)
browser.maximize_window()
browser.get(url)

movies=[]
urlStart="https://yts.am/movie/"
urlEnd=[]

mList=browser.find_elements_by_class_name("lister-item-content")

if len(mList)==0:
    file.write("Error loading page. Seems like Internet Problem.\n\n")
    browser.quit()
    file.close()
    sys.exit()
    
for i in mList:
    temp=i.find_elements_by_tag_name("span")
    year=temp[1].get_attribute("innerHTML").strip()
    temp=i.find_elements_by_tag_name("a")
    title=temp[0].get_attribute("innerHTML").strip()
    movies.append(title+" "+year)
    title1=title.lower().replace(" ","-")
    year1=year[1:(len(year)-1)]
    urlEnd.append(title1+"-"+year1)

browser.quit()

file.write("Movies in Download List :\n")
for i in movies:
    file.write(i+"\n")

for i in range(0,len(urlEnd)):
    if isTorrentPresent(movies[i]+".torrent","C:\\Users\\rays\\Documents\\Automation Torrents"):#path where torrents are present
        file.write(movies[i]+" torrent already downloaded. Movie download in progress.\n")
        continue
    res=requests.get(urlStart+urlEnd[i])
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    elem=soup.select("#movie-info > p > a")
    if len(elem)==0:
        file.write(movies[i]+" not present currently in YTS database.\n")
        continue
    link=elem[0]['href']
    for j in elem:
        if j['title'].find('720p')!=-1 :
            link=j['href']
            break
    
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'CERN-LineMode/2.15 libwww/2.17b3')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(link, 'C:\\Users\\rays\\Documents\\Automation Torrents\\'+movies[i]+".torrent")#path where torrents are downloaded and saved
        file.write("Succesfully downloaded "+movies[i]+" torrent.\n")
        os.startfile('C:\\Users\\rays\\Documents\\Automation Torrents\\'+movies[i]+".torrent")
        file.write("Started downloading "+movies[i]+"\n")
    except:
        file.write("Error in downloading torrent file\n")

done=[]
for i in range(0,len(movies)):
    if isMoviePresent(movies[i],"C:\\Users\\rays\\Documents\\Automation Completed Downloads"):#path where movies are transferred after download has finished
        done.append(True)
    else:
        done.append(False)

removeFromList(done)
removeTorrent(done)
file.write("Script successfully executed.\n\n")
file.close()

#Code Ends.
#coolyansh
