import random
import os
import time

PROXY_IP = "172.18.0.2:8000"
PROXY_SWITCH_TIME = 180


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
"US Arkansas","US Atlanta","US Baltimore","US California","US Chicago","US Connecticut","US Denver","US East","US East Streaming Optimized",
"US Florida","US Honolulu","US Houston","US Idaho","US Indiana","US Iowa","US Kansas","US Kentucky","US Las Vegas","US Louisiana","US Maine",
"US Massachusetts","US Michigan","US Minnesota","US Mississippi","US Missouri","US Montana","US Nebraska","US New Hampshire","US New Mexico",
"US New York","US North Carolina","US North Dakota","US Ohio","US Oklahoma","US Oregon","US Pennsylvania","US Rhode Island","US Salt Lake City",
"US Seattle","US Silicon Valley","US South Carolina","US South Dakota","US Tennessee","US Texas","US Vermont","US Virginia","US Washington DC",
"US West","US West Streaming Optimized","US West Virginia","US Wilmington","US Wisconsin","US Wyoming","Ukraine","United Arab Emirates","Uruguay",
"Venezuela","Vietnam"]

regionNum = random.randrange(0,len(piaRegions))
region = piaRegions[regionNum]

while True:
    command = "curl -X PUT "+ PROXY_IP +"/v1/vpn/settings -H \'Content-Type: application/json' -d \'{\"provider\": {\"server_selection\": {\"regions\": [\""+ region + "\"]}}}\'"
    os.system(command)
    print(f"Switched to:{region}")
    time.sleep(PROXY_SWITCH_TIME)
    regionNum = (regionNum + 1) % len(piaRegions)
    region = piaRegions[regionNum]
