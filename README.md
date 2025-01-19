# Sankalp Awasthi Assessment 

# Approach and Solution from SDLC point of view
1. Parsing the 2 Datasets of Logs and Lookup Table
2. Fixing the Protocol[number] = Protocol[name] while parsing
3. Changing the Lookup Table dataset to hashmap for faster access to values from keys
4. keys formed from (dstport+protocol) and values as the (tags) = Lookup Hashmap
5. These logs are readed line by line and there dstport+protocol is matched with Hashmap keys
6. if no key is matched the combo is "Untagged" and the main logs those enteries as called as untags
7. if Key is found its value that is tag is stored and that combo counter increments by 1
8. if more same key is hits the combo key is incremented and stored in combo dictionary and same goes for tags
9. same if tags are found it will get incremented and got stored in tag dictionary

# Assumptions Made 
1. The Lookup table data and Logs are independent and then we have to match the logs to the table and do the needfull operation
2. the combo of dstport and protocol will tell tags , those tags have been handled in the dataset
3. The Untagged count are those enteries whose dstport,protocol is not found in the LookupTable , thus untagged
4. the count for dstport,protocol is not total count from logs but the ones those are getting the tags hit via lookup

# Low Level Design of the Application 

![image](https://github.com/user-attachments/assets/044425c8-0d44-40da-97e0-056cb2e759bd)

# Running Instruction 
1. Developed in VSC Environment
2. Just download this folder or clone this repo
3. go to the Folder "Illumino SankalpAwasthi" and Open in side explorer
4. run the index.py file (Dataset folder should be there as well, contains both db1,db2 txt files)[to show simple execution followed the function in same file otherwise rom SDLC POV , it should be all function in separate py fikle and importing and calling them from main file]
5. Output.txt will be generated in the Output folder , Location of output = "Output/output.txt"


