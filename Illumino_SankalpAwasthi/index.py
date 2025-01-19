#Constants
protocols = ["HOPOPT", "ICMP", "IGMP", "GGP", "IPv4", "ST", "TCP", "CBT", "EGP", "IGP", "BBN-RCC-MON", "NVP-II", "PUP", "ARGUS (deprecated)", "EMCON", "XNET", "CHAOS", "UDP", "MUX", "DCN-MEAS", "HMP", "PRM", 
             "XNS-IDP", "TRUNK-1", "TRUNK-2", "LEAF-1", "LEAF-2", "RDP", "IRTP", "ISO-TP4", "NETBLT", "MFE-NSP", "MERIT-INP", "DCCP", "3PC", "IDPR", "XTP", "DDP", "IDPR-CMTP", "TP++", "IL", "IPv6", "SDRP", "IPv6-Route", 
             "IPv6-Frag", "IDRP", "RSVP", "GRE", "DSR", "BNA", "ESP", "AH", "I-NLSP", "SWIPE (deprecated)", "NARP", "MOBILE", "TLSP", "SKIP", "IPv6-ICMP", "IPv6-NoNxt", "IPv6-Opts", "any host internal protocol", "CFTP", 
             "any local network", "SAT-EXPAK", "KRYPTOLAN", "RVD", "IPPC", "any distributed file system", "SAT-MON", "VISA", "IPCV", "CPNX", "CPHB", "WSN", "PVP", "BR-SAT-MON", "SUN-ND", "WB-MON", "WB-EXPAK", "ISO-IP", 
             "VMTP", "SECURE-VMTP", "VINES", "IPTM", "NSFNET-IGP", "DGP", "TCF", "EIGRP", "OSPFIGP", "Sprite-RPC", "LARP", "MTP", "AX.25", "IPIP", "MICP (deprecated)", "SCC-SP", "ETHERIP", "ENCAP", "any private encryption scheme", 
             "GMTP", "IFMP", "PNNI", "PIM", "ARIS", "SCPS", "QNX", "A/N", "IPComp", "SNP", "Compaq-Peer", "IPX-in-IP", "VRRP", "PGM", "any 0-hop protocol", "lookupTableTP", "DDX", "IATP", "STP", "SRP", "UTI", "SMP", "SM (deprecated)", "PTP", 
             "ISIS over IPv4", "FIRE", "CRTP", "CRUDP", "SSCOPMCE", "IPLT", "SPS", "PIPE", "SCTP", "FC", "RSVP-E2E-IGNORE", "MobilityHeader", "UDPLite", "MPLS-in-IP", "manet", "HIP", "Shim6", "WESP", "ROHC", 
             "Ethernet"] + ["Unassigned"] * 109 + ["Use for experimentation and testing"] * 2 + ["Reserved"]

#Created a constant list for mapping the protocols to their respective numbers

#Function to read the data from the logs and lookup file
def readData(logLocation,lookupLocation):

    logFile = open(logLocation,"r")
    logsChannel = logFile.readlines()

    #Creating a 2D array of logs for easy access of fields
    logs = [x.split(",") for x in logsChannel] 

    #Mapping the protocol numbers to their respective names in lower case from the protocols list[Constants]
    for i in range(len(logs)):
        logs[i][7] = protocols[int(logs[i][7])].lower() 

    lookup_file = open(lookupLocation,"r")
    lookupTable = lookup_file.readlines()

    return logs, lookupTable

#Funtion to convert the lookup table to a hash map for easy access and faster search Optiminsed from traditional big(M*N)
def lookupHashMap(lookupTable):

    lookup_dict={}
    #the key is ["port,protocol"] and value is the "tag"
    for i in range(len(lookupTable)):
        line = lookupTable[i].split(",")
        lookup_dict[line[0]+","+line[1]] = line[2]

    return lookup_dict


#Function to match the logs with the lookup table and count the number of times a tag is hit 
def matchOperation(logs, lookup_dict):
    
    #counter for tags hitting in the logs
    tag_counter = {}

    #counter for port and protocol combinations that gets hits
    port_protocol_counter={}

    for i in range(len(logs)):

        #creating a key for the lookup table and storing it in variable port_protocol , 6 and 7 are the dstport and protocol respectively in logs field 
        port_protocol = logs[i][6]+","+logs[i][7]
        try:
            #Storing that combo of port and protocol in key
            key = lookup_dict[port_protocol]
        except:
            #if that combo does not exist in the lookup table then it is untagged
            key = "Untagged\n"

        #Counting the number of times a tag is hit via key   
        if key in tag_counter:
            tag_counter[key]+=1
        else:
            #its 1 as its the first time the key is getting hit
            tag_counter[key]=1

        #if the key is not untagged then we need to count the number of times a port , protocol combo is hit    
        if key!= "Untagged\n":
            if port_protocol in port_protocol_counter:
                port_protocol_counter[port_protocol]+=1
            else:
                port_protocol_counter[port_protocol]=1
    
    #returning the two counters
    return tag_counter, port_protocol_counter


#Output function to write the data to a file
def writeOutput(tag_counter, port_protocol_counter,logs):


    output = open("Output/output.txt", "w")

    #writing the total number of hits for each tag(not including untagged)
    output.write("Total tags hit: " + str(len(logs) - tag_counter["Untagged\n"]) + "\n")
    output.write("Tag,Counts: \n")

    #Printing the tag(-1 beacuse eliminated the extra"\n" generated while paraing the txt) and the number of times it got hit
    for x in tag_counter:
        output.write(x[:-1]+","+str(tag_counter[x])+"\n")

    #counter for port and protocol combinations that gets hits
    port_portocol_comsCounter =0
    for x in port_protocol_counter:
        port_portocol_comsCounter+= port_protocol_counter[x]

    output.write("\n\n")
    output.write("Total port protocol combinations hits: " + str(port_portocol_comsCounter) + "\n" )

    output.write("Port,Protocol,Count: \n")

    #Printing the port and protocol combo and the number of times it got hit
    for x in port_protocol_counter:
        output.write(x+","+ str(port_protocol_counter[x])+"\n")

    output.close()


def main():
    try:
        
        #Dataset Locations
        logLocation = "Dataset/Logs.txt"
        lookupLocation = "Dataset/Lookup.txt"

        #Reading the data from the logs and lookup file with protocols adjusted to their respective names
        logs, lookupTable = readData(logLocation,lookupLocation)

        #Loopup Table Hash Map
        lookup_dict = lookupHashMap(lookupTable)

        #Matching the logs with the lookup table and counting the number of times a tag is hit
        tag_counter, port_protocol_counter = matchOperation(logs, lookup_dict)

        #Output the data to a file
        writeOutput(tag_counter, port_protocol_counter,logs)
        print("Processing complete. Results written to Floder = [Output] containing file= '{'output.txt'}' ")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

