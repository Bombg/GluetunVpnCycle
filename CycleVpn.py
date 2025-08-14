import random
import os
import time
import docker
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    PROXY_IP:str = "127.0.0.1:8000"
    SWITCH_GLUETUN:bool = True
    LOOP_WAIT_TIME:int = 180
    CONTAINER_NAME:str = "gluetun-gluetun-1"
    SOCKS5_CONTAINER_NAME:str = "gluetun-socks5-1"
    CONTAINER_RESTART_WAIT:int = 30
    SCRIPT_START_TIME:ClassVar[int] = time.time()
    TIME_BEFORE_RESTART:int = 86400
    piaRegions:ClassVar[list[str]] = ["Albania", "Algeria", "Andorra", "Argentina", "Armenia", "Austria", "Bahamas", "Belgium", "Bolivia", "Bosnia and Herzegovina", 
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

baseSettings = Settings()
regionNum = random.randrange(0,len(baseSettings.piaRegions))
region = baseSettings.piaRegions[regionNum]
client = docker.from_env()
nonRestartStatuses = ['healthy', 'running', 'starting', 'created', 'paused', 'restarting', 'removing']

def SwitchGluetunRegion():
    global region
    global regionNum
    command = "curl -X PUT "+ baseSettings.PROXY_IP +"/v1/vpn/settings -H \'Content-Type: application/json' -d \'{\"provider\": {\"server_selection\": {\"regions\": [\""+ region + "\"]}}}\'"
    os.system(command)
    #print(f"Switched to:{region}")
    regionNum = (regionNum + 1) % len(baseSettings.piaRegions)
    region = baseSettings.piaRegions[regionNum]

def RestartAndClean(client):
    client.images.prune(filters={'dangling': False})
    print("rebooting server")
    os.system('reboot')

if __name__ == "__main__":
    while True:
        # container.attrs['State']['Health']['Status'] -- for health status. .status only has basic statuses
        #print("_________________________________________________________________________________________")
        containers = client.containers.list(all=True)
        for container in containers:
            if container.status.lower() not in nonRestartStatuses:
                print(f"{container.status}:{container.name} restarting container")
                container.restart()
                time.sleep(baseSettings.CONTAINER_RESTART_WAIT)
        if baseSettings.SWITCH_GLUETUN:
            SwitchGluetunRegion()
        time.sleep(baseSettings.LOOP_WAIT_TIME)
        timeSinceStart = time.time() - baseSettings.SCRIPT_START_TIME
        #print(f"TimeSinceStart:{timeSinceStart}")
        if timeSinceStart >= baseSettings.TIME_BEFORE_RESTART:
            RestartAndClean(client)
    
