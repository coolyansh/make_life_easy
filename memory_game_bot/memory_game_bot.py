#Works with 1366*768 resolution
#Open the game in any browser and scroll down to the bottom. Make changes according to the pixel position.

import pyautogui, os
from time import sleep

def findName(x):
    flag="No Match Found"
    for root,dirs,file in os.walk("images"):
        for filename in file:
            if pyautogui.locate(root+"\\"+filename,x,grayscale=True):
                flag=filename[0:filename.find(".")]
                break

    return flag

def findPair(nm,pos):
    for i in range(0,16):
        if i==pos:
            continue
        if nm==name[i]:
            break
    return i

print("--------------------------------------------------\nStarting Memory Game Bot .....")
pyautogui.click(567,775)#position(pixels) of Google Chrome icon in Taskbar(where game site is already loaded)
pyautogui.click(677, 72)#position(pixels) of refresh icon in the game
row=450
col=180
im=[]
name=[]
clickpos=[]

for i in range(0,4):
    for j in range(0,4):
        i1=row+j*150
        j1=col+i*150
        clickpos.append([i1,j1])
        
for i in range(0,16):
    i1=clickpos[i][0]
    j1=clickpos[i][1]
    clickpos.append([i1,j1])
    pyautogui.click(i1,j1)
    sleep(0.4)
    im.append(pyautogui.screenshot(region=(i1-150,j1-150,i1+150,j1+150)))
    im[i].save(str(i)+".PNG")
    res=findName(str(i)+".PNG")
    print(str(i)+" "+res,end=' ')
    name.append(res)
    try:
        ind=name.index(res)
    except:
        print("Error while finding index.")
    if i!=ind:
        print("Previously found at "+str(ind))
        pyautogui.click(i1,j1,duration=0.1)
        pairpos=clickpos[ind]
        pyautogui.click(pairpos[0],pairpos[1],duration=0.1)
    else:
        print("Previously not there")

        
print("Board configuration is :\n")
for i in range(0,4):
    for j in range(0,4):
        print('{:<15}'.format(name[i*4+j]),end=' ')
    print()

print("\nMemory Game Completed Successfully.")
sleep(2)
pyautogui.click(567,775)
print("--------------------------------------------------\nMade by coolyansh\n\n")
input("Press any key to quit")

