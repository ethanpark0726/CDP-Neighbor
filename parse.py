import re

class Parse:
    def __init__(self, data, os):

        self.data = data
        self.result = {}
        self.os = os

    def getOS(self):
        return self.os
    
    def getInterfaceList(self, os):

        pattern = re.compile('(Eth|Gi|Te|Tw|mg)')
        interfaceList = []

        if os == 'IOS':
            for elem in self.data[2:len(self.data) - 1]:
                match = pattern.search(elem)
                
                if match:
                    split = elem.split(' ')
                    split = list(filter(None, split))

                    if pattern.search(split[0]):
                        interfaceList.append(' '.join(split[0:2]))
                    else:
                        interfaceList.append(' '.join(split[1:3]))
            

        elif os == 'NXOS':
            for elem in self.data[2:len(self.data) - 1]:
                match = pattern.search(elem)
                            
                if match:
                    split = elem.split(' ')
                    split = list(filter(None, split))
        
                    if pattern.search(split[0]):
                        interfaceList.append(' '.join(split[0:1]))
                    else:
                        interfaceList.append(' '.join(split[1:2]))
        
        return interfaceList

    def getBaseDescription(self, interfaceList):
        
        parsedInterfaceList = list()

        for elem in interfaceList:
            newID = list(elem.values())[0].split(":")[-1].strip()

            # Clean up DeviceName.shands.ufl.edu pattern
            newID = newID.split('.')[0]

            # Clean up DeviceName(SerialNumber) pattern
            newID = newID.split('(')[0]

            # Skip Cisco APs data
            obj = re.compile(r'^(AP)|^(AC)|^(AT)|^\d|^S|^a|^(el)|^(uf)|^b|^t')

            if obj.search(newID) == None:
                elem[list(elem.keys())[0]] = newID
                parsedInterfaceList.append(elem)

        print("--- Device ID Extraction success")   
        return parsedInterfaceList
