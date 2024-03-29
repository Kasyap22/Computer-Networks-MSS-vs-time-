"""Code for plotting MSS vs Time
   Team Members: 
                 C Sai Kasyap(Reg No. 190905084), Section and Roll No. CSE-B 14, Lab Batch: 1
                 Venkata Naga Sai Rohit Kanteti(Reg No. 190905314), Section and Roll No. CSE-B 46, Lab Batch: 3
"""

import dpkt
import os
import sys
import socket
import datetime
import struct
from  datetime import datetime as dtime
import matplotlib.pyplot as plt

#method to get the MSS size from the options field of TCP header
def get_MSS(options) :
    options_list = dpkt.tcp.parse_opts ( options )
    for option in options_list :
        if option[0] == 2 :
            mss = struct.unpack(">H", option[1])
            return mss[0]

#Method to extract the payload prsent in the  packets of different layers    
def parsePcap(pcap):
    mss=[]
    time=[]
    cnt = 0
    pkt_cnt = 0
    for (ts,buf) in pcap:

        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            if ip.p==dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data
                pkt_cnt += 1
                m = get_MSS(tcp.opts)
                if m==None:
                    cnt+=1
                    continue
                    # mss.append(m)
                mss.append(m)
                temp = str(datetime.datetime.utcfromtimestamp(ts))
                time_string = temp[11:19]
                date_time = dtime.strptime(time_string, "%H:%M:%S")
                a_timedelta = date_time - datetime.datetime(1900, 1, 1)
                seconds = a_timedelta.total_seconds()
                time.append(seconds)
        except Exception as e:
            print("Error!",e)
            sys.exit(1)
            
    #IF no packet found with MSS or no SYN packet found
    if cnt==pkt_cnt:
        print("No packets found with MSS info")
        sys.exit(1)
    print(len(time),len(mss))
    t = time[0]
    for i in range(len(time)):
        time[i] -= t
   
    print("MSS:",*mss)
    print("Time:",*time)
    #plot graph
    plt.plot(time,mss,color='b')
    plt.scatter(time,mss,color='k')
    plt.title('MSS vs time')
    plt.xlabel('time')
    plt.ylabel('MSS')
    plt.show()

def main():
    file_name = input("Enter the pcap filename or pathname: ")
    try:
        f = open(file_name,'rb')
        pcap = dpkt.pcap.Reader(f)
    except Exception as e:
        print("Error!",e)
        sys.exit(1)
    try:
        parsePcap(pcap)
    except Exception as e:
        print("Error!",e)

if __name__== "__main__":
    main()