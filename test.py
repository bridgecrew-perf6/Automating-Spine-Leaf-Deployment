from cgitb import enable
from nornir.core.task import Task, Result
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_napalm.plugins.tasks import napalm_get
from microsegmenter import MicroSegmenter
import time
from pingTest import ping
from resett import resetter, resettHostName

#todo:
#1. make a enviroment reset function that compleatly resetts the enviroment back to basic functionality
#2. tftp ssh deployment using option 82 (optional)
#3. client side almoaste equal settup, only difrence is in host. yaml file

startTime=time.time() #this is the start time of the program

def main():

    bringDown=False
    oneHost=False

    nr = InitNornir(config_file="config.yaml") #this is the nornir object
    if oneHost:
        nr = nr.filter(name="spine2.cmh") #this is the nornir object with only one host

    if bringDown:
        nr.run(task=ping)
        print("configuring hostnames and ip domain name")
        nr.run(task=resettHostName)
        nr = InitNornir(config_file="config.yaml") #re initialize the nornir object due to changes in hostname breaking the rest of the program if not reinitialized
        if oneHost:
            nr = nr.filter(name="spine2.cmh") #this is the nornir object with only one host
        nr.run(task=resetter)

    else:
        nr.run(task=ping)
        nr.run(task=MicroSegmenter,SegmentationIps="10.0",
            SpineHostName="spine", 
            LeafHostname="leaf", 
            IpDomainName="simon")


main() #run the main function


print(f"\n\n\n\n\n\n\n\n\n\nthe script took {time.time()-startTime} seconds") #prints how long the script took to run