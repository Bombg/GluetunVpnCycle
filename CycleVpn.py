import random
import os
import time
import docker

PROXY_IP = "127.0.0.1:8000"
PROXY_SWITCH_TIME = 180
CONTAINER_NAME = "gluetun-gluetun-1"
CONTAINER_RESTART_WAIT = 30
SCRIPT_START_TIME = time.time()
TIME_BEFORE_RESTART = 86400

piaRegions = ["AU Adelaide","AU Brisbane","AU Melbourne","AU Perth","AU Sydney","Albania","Algeria","Andorra","Argentina","Armenia",
"Australia Streaming Optimized","Austria","Bahamas","Bangladesh","Belgium","Bolivia","Bosnia and Herzegovina",
"Brazil","Bulgaria","CA Montreal","CA Ontario","CA Ontario Streaming Optimized","CA Toronto","CA Vancouver",
"Cambodia","Chile","China","Colombia","Costa Rica","Croatia","Cyprus","Czech Republic","DE Berlin","DE Frankfurt",
"DE Germany Streaming Optimized","DK Copenhagen","DK Streaming Optimized","ES Madrid","ES Valencia","Ecuador","Egypt",
"Estonia","FI Helsinki","FI Streaming Optimized","France","Georgia","Greece","Greenland","Guatemala","Hong Kong","Hungary",
"IT Milano","IT Streaming Optimized","Iceland","India","Indonesia","Ireland","Isle of Man","Israel","JP Streaming Optimized",
"JP Tokyo","Kazakhstan","Latvia","Liechtenstein","Lithuania","Luxembourg","Macao","Malaysia","Malta","Mexico","Moldova","Monaco",
"Mongolia","Montenegro","Morocco","NL Netherlands Streaming Optimized","Nepal","Netherlands","New Zealand","Nigeria",
"North Macedonia","Norway","Panama","Peru","Philippines","Poland","Portugal","Qatar","Romania","SE Stockholm",
"SE Streaming Optimized","Saudi Arabia","Serbia","Singapore","Slovakia","Slovenia","South Africa","South Korea","Sri Lanka",
"Switzerland","Taiwan","Turkey","UK London","UK Manchester","UK Southampton","UK Streaming Optimized","US Alabama","US Alaska",
"US Atlanta","US Baltimore","US California","US Chicago","US Connecticut","US Denver","US East","US East Streaming Optimized",
"US Florida","US Honolulu","US Houston","US Idaho","US Indiana","US Iowa","US Kansas","US Kentucky","US Las Vegas","US Maine",
"US Massachusetts","US Michigan","US Minnesota","US Missouri","US Nebraska","US New Hampshire","US New Mexico",
"US New York","US North Dakota","US Ohio","US Oklahoma","US Oregon","US Pennsylvania","US Rhode Island",
"US Seattle","US Silicon Valley","US South Carolina","US South Dakota","US Tennessee","US Vermont","US Washington DC",
"US West","US West Streaming Optimized","US West Virginia","US Wilmington","US Wisconsin","US Wyoming","Ukraine","United Arab Emirates","Uruguay",
"Venezuela","Vietnam"]

regionNum = random.randrange(0,len(piaRegions))
region = piaRegions[regionNum]
client = docker.from_env()
gluetunContainer = client.containers.get(CONTAINER_NAME)
gluetunState = gluetunContainer.attrs['State']['Health']['Status']

while True:
    print("_____________________________________________________________________________")
    print(f"Status:{gluetunState}")
    if not gluetunState or gluetunState == "unhealthy":
        print("Container unhealthy, restarting container")
        gluetunContainer.restart()
        time.sleep(CONTAINER_RESTART_WAIT)
    command = "curl -X PUT "+ PROXY_IP +"/v1/vpn/settings -H \'Content-Type: application/json' -d \'{\"provider\": {\"server_selection\": {\"regions\": [\""+ region + "\"]}}}\'"
    os.system(command)
    print(f"Switched to:{region}")
    time.sleep(PROXY_SWITCH_TIME)
    timeSinceStart = time.time() - SCRIPT_START_TIME
    print(f"TimeSinceStart:{timeSinceStart}")
    if timeSinceStart >= TIME_BEFORE_RESTART:
        print("rebooting server")
        os.system('reboot')
    regionNum = (regionNum + 1) % len(piaRegions)
    region = piaRegions[regionNum]
    gluetunContainer = client.containers.get(CONTAINER_NAME)
    gluetunState = gluetunContainer.attrs['State']['Health']['Status']
