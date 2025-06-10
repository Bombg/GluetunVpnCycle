import random
import os
import time
import docker

PROXY_IP = "127.0.0.1:8000"
PROXY_SWITCH_TIME = 180
CONTAINER_NAME = "gluetun-gluetun-1"
SOCKS5_CONTAINER_NAME = "gluetun-socks5-1"
CONTAINER_RESTART_WAIT = 30
SCRIPT_START_TIME = time.time()
TIME_BEFORE_RESTART = 86400

piaRegions = ["Albania", "Algeria", "Andorra", "Argentina", "Armenia", "Austria", "Bahamas", "Belgium", "Bolivia", "Bosnia and Herzegovina", 
                "Brazil", "Bulgaria", "CA Montreal", "CA Ontario", "CA Ontario Streaming Optimized", "CA Toronto", "CA Vancouver", "Cambodia", "Chile", "Colombia", 
                "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "DE Berlin", "DE Frankfurt", "DE Germany Streaming Optimized", "DK Copenhagen", 
                "DK Streaming Optimized", "ES Madrid", "ES Valencia", "Ecuador", "Estonia", "FI Helsinki", "FI Streaming Optimized", "Georgia", "Greece", "Greenland", 
                "Guatemala", "Hong Kong", "Hungary", "IT Milano", "IT Streaming Optimized", "Iceland", "Ireland", "Isle of Man", "Israel", "JP Streaming Optimized", 
                "JP Tokyo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Malta", "Mexico", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
                "NL Netherlands Streaming Optimized", "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia", "Norway", "Panama", "Peru", "Poland", "Portugal", 
                "Romania", "SE Stockholm", "SE Streaming Optimized", "Serbia", "Slovakia", "Slovenia", "South Africa", "South Korea", "Switzerland", "Taiwan", "Turkey", "US Alaska", 
                "US Atlanta", "US Baltimore", "US California", "US Chicago", "US Connecticut", "US Denver", "US East", "US East Streaming Optimized", "US Honolulu", "US Houston", "US Las Vegas", 
                "US Maine", "US Massachusetts", "US Michigan", "US Minnesota", "US New Hampshire", "US New Mexico", "US New York", "US North Dakota", "US Ohio", "US Oregon", "US Pennsylvania", 
                "US Rhode Island", "US Seattle", "US Silicon Valley", "US Vermont", "US Washington DC", "US West", "US West Streaming Optimized", "US Wilmington", "US Wisconsin", "US Wyoming", 
                "Ukraine", "Uruguay", "Venezuela"]

regionNum = random.randrange(0,len(piaRegions))
region = piaRegions[regionNum]
client = docker.from_env()
gluetunContainer = client.containers.get(CONTAINER_NAME)
socks5Container = client.containers.get(SOCKS5_CONTAINER_NAME)
gluetunState = gluetunContainer.attrs['State']['Health']['Status']

while True:
    print("_____________________________________________________________________________")
    print(f"Status:{gluetunState}")
    if not gluetunState or gluetunState == "unhealthy":
        print("Container unhealthy, restarting container")
        gluetunContainer.restart()
        time.sleep(CONTAINER_RESTART_WAIT)
    command = "curl -X PUT "+ PROXY_IP +"/v1/vpn/settings -H \'Content-Type: application/json' -d \'{\"provider\": {\"server_selection\": {\"regions\": [\""+ region + "\"]}}}\'"
    time.sleep(5)
    socks5Container.restart()
    os.system(command)
    print(f"Switched to:{region}")
    time.sleep(PROXY_SWITCH_TIME)
    timeSinceStart = time.time() - SCRIPT_START_TIME
    print(f"TimeSinceStart:{timeSinceStart}")
    if timeSinceStart >= TIME_BEFORE_RESTART:
        client.images.prune(filters={'dangling': False})
        print("rebooting server")
        os.system('reboot')
    regionNum = (regionNum + 1) % len(piaRegions)
    region = piaRegions[regionNum]
    gluetunContainer = client.containers.get(CONTAINER_NAME)
    socks5Container = client.containers.get(SOCKS5_CONTAINER_NAME)
    gluetunState = gluetunContainer.attrs['State']['Health']['Status']
