import requests
import bs4, sys
from time import sleep
from pygame import mixer

def fetchData(url,selector,count):
    try:
        res=requests.get(url,timeout=10)
        res.raise_for_status()
    except:
        print("Error in fetching data from Cricbuzz. Will try again after 10 seconds.")
        return -1
    
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    elem=soup.select(selector)
    if len(elem)==0:
        return 0

    if count%20==0:
        print("Current match status :")
        tname=elem[0].select("div.cb-col.cb-col-100.cb-scrd-hdr-rw > span:nth-of-type(1)")
        print(tname[0].text.strip())
        tscore=elem[0].select("div.cb-col.cb-col-100.cb-scrd-hdr-rw > span:nth-of-type(2)")
        print(tscore[0].text.strip())
    

    items=elem[0].select("div.cb-col.cb-col-100.cb-scrd-itms")

    past=[]
    present=[]
    over=[]
    future=[]
    for i in range(0,len(items)):
        nm=items[i].select("div:nth-of-type(1)")
        ind=nm[0].text.find('(')
        if ind==-1:
            ind=len(nm[0].text)
        name=nm[0].text[:ind].strip()
        if name=="Extras" or name=="Total":
            continue
        elif name=="Yet to Bat" or name=="Did not Bat":
            out=items[i].select("div:nth-of-type(2) > a")
            for j in out:
                ind=j.text.find('(')
                if ind==-1:
                    ind=len(j.text)
                future.append(j.text[:ind].strip())
        else:
            ot=items[i].select("div:nth-of-type(2)")
            out=ot[0].text.strip()
            if out=="batting":
                present.append(name)
            elif out=="not out":
                over.append(name)
            else:
                past.append(name)


    if batsman in future:
        return 1

    elif batsman in past:
        return 2

    elif batsman in over:
        return 3
    
    else:
        return 4
    
mixer.init()
mixer.music.load('Yanni - Last of the Mohicans Theme.mp3')
print("\n------X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X------\n")
print("WELCOME TO \"ALERT ME WHEN BATSMAN COMES TO BAT\" SCRIPT\nTO USE THIS SCRIPT YOU NEED TO ENTER THE URL OF THE ONGOING MATCH(SCOREBOARD URL OF CRICBUZZ) AND THE NAME OF THE BATSMAN(AS ON CRICBUZZ SITE).")
print("THAT'S IT. YOU WILL BE ALERTED AS SOON THE BATSMAN COMES TO BAT.")
print("\n\n\t\t\t\t\t Developed by coolyansh\n")
print("\n------X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X------\n")
print("Enter URL of match \nExample:- https://www.cricbuzz.com/live-cricket-scorecard/20309/aus-vs-rsa-2nd-odi-south-africa-tour-of-australia-2018 \nURL should start with \"https://www.cricbuzz.com/live-cricket-scorecard/\"")
urlAdd=input()

try:
    res=requests.get(urlAdd,timeout=10)
    res.raise_for_status()
except:
    print("Error in retrieving URL .\nPlease check your URL address or your internet conection")
    input("Press ENTER to exit")
    sys.exit()

soup=bs4.BeautifulSoup(res.text,"html.parser")
elem1=soup.find_all("div", class_="cb-col cb-scrcrd-status cb-col-100 cb-text-live")
elem2=soup.find_all("div", class_="cb-col cb-scrcrd-status cb-col-100 cb-text-complete")
elem3=soup.find_all("div", class_="cb-col cb-col-100 cb-font-16 cb-scrcrd-status")

flag=0

if len(elem2)!=0:
    print("Match is already over.\n"+elem2[0].text+"\nYou should have used our script earlier. \n")
elif len(elem3)!=0:
    print("Match has not yet started.Please run this script when the match starts")
elif len(elem1)!=0:
    print("Script in Progress\n"+elem1[0].text)
    flag=1
else:
    print("Please enter valid match URL. PLEASE.")

if flag==0:
    input("Press ENTER to exit")
    sys.exit()

team1=[]
team2=[]

t1=soup.find_all("div",class_="cb-col cb-col-100 cb-minfo-tm-nm")
t2=soup.find_all("div",class_="cb-col cb-col-100 cb-minfo-tm-nm cb-minfo-tm2-nm")
ind=t1[0].text.find("Squad")
tname1=t1[0].text[:ind].strip()
ind=t2[0].text.find("Squad")
tname2=t2[0].text[:ind].strip()

temp=t1[1].find_all("a")
for i in temp:
    tmp=i.text
    end=tmp.find('(')
    if end==-1:
        team1.append(tmp.strip())
    else:
        team1.append(tmp[:end].strip())

temp=t1[3].find_all("a")
for i in temp:
    tmp=i.text
    end=tmp.find('(')
    if end==-1:
        team2.append(tmp.strip())
    else:
        team2.append(tmp[:end].strip())

print("Enter name of batsman as on cricbuzz website ")
batsman=input()
team=""
if batsman in team1:
    team=tname1
elif batsman in team2:
    team=tname2
else:
    print(batsman+" is not playing the match")
    input("Press ENTER to exit")
    sys.exit()

print(batsman+" plays for "+team)

elem=soup.select("#innings_1 > div:nth-of-type(1)")
tnm=elem[0].select("div.cb-col.cb-col-100.cb-scrd-hdr-rw > span:nth-of-type(1)")
ind=tnm[0].text.find("Innings")
tname=tnm[0].text[:ind].strip()

if tname==team:
    selector="#innings_1 > div:nth-of-type(1)"
else:
    selector="#innings_2 > div:nth-of-type(1)"

count=0
interval=0
while True:
    result=fetchData(urlAdd,selector,count)
    if result==-1:
        interval=10
    elif result==0:
        print(team+" Innings not started. Script will check status again after 3 minutes.")
        interval=60*3
    elif result==1:
        print(batsman+" is still waiting in dugout. Script will check status again after 30 seconds.") 
        interval=30
    elif result==2:
        print(batsman+" is already in pavillion. Feeling sorry for you.\nScript will end now.")
        break
    elif result==3:
        print(batsman+" remained not out but his innings is over.\Script will end now.")
        break
    else:
        print(batsman+" has arrived on the crease.\nSounding the Alarm now.\nTune in your TV(or your phone) and enjoy his batting.\n")
        mixer.music.play(-1)
        break

    sleep(interval)
    count+=1

print("Thanks for using this script.\nHope you enjoyed using it.\n\t\t\t\t---coolyansh\n")
input("Press Enter to exit")
sys.exit()

