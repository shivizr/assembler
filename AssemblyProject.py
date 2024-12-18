FinalOPcode=[] #holding the final opcode of all instructions
labels=[]      #a list of labels 
instructions=[] #a list of instructions 
counterLabel=0 #to count the number of each instructions that is assembled between the definition of the label and jump to that label(for the backeard jump)
LabelFlag=False #it uses for the forward jump
flag=False #for the backward jump if the label was available
counter=0 #it's the counter of instruction for the forward jump
microcontroller=["XX"]*256   #as the microcontroller 
pointerStack=0    # the pointer for the stack and initialize 0
pointerData=100   #the pointer for the data and initialize 100
pointerCode=200   #the pointer for the code and initialize 200
stackFlag=False   #to check if it is in the stack part of the input
dataFlag=False    #to check if it is in the data part of the input
codeFlag=False    #to check if it is in the code part of the input
startStack=0
startData=100
startCode=200
Reg8=['al','cl','dl','bl','ah','ch','dh','bh'] #list of 8_bit register
Reg16=['ax','bx','cx','dx','si','di','bp','sp'] #list of 16_bit register
Reg32=['eax','ebx','ecx','edx','ebp','esp','esi','edi'] #list of 32_bit register
indirect = False
print("Which way you want to read data from:1-file 2-CommandLine...or 3-Exit")
num=int(input())
flagSpace=0
if num == 1: #if the input should be read from a file
    path=input("Enter the path of the file: ") #get the path of the file and hold it in the path
    with open(path, "r") as file: #read the file
        instructions = file.readlines()  #hold each line a part as a string in instructions list
elif (num == 2): #if instructions should be read from the command line and store it in instructions list
    while(1):
        Instruction=input("Enter the instruction you want to assemble(if there is no instruction to assemble just press enter): ")
        if (not Instruction):
            break
            #if there was no line or instructions as input (or enter) it will break the while loop
        else:
            instructions.append(Instruction) #each instruction that read from the command line it will add to the list of instruction
LineCounter=len(instructions) #calculate the number of instructions in the list
for i in range(LineCounter):
    Instruction = "" #an empty string to hold each instruction of the instructions list
    Counter=0 #to not calculate the first white space of an instruction
    flagSpace=False #a flag to check the white space of the instruction
    for element in instructions[i]: #a for loop to add the i th elemnt of the instructions list to Instruction 
        if element == ' ' and flagSpace == False and Counter <= len(instructions[i]): #to don't add the first whitespace of the instructions to the Instruction
            Counter+=1
        elif element != '\n': #if at the end of the instruction there was a '\n' or new line character
            flagSpace=True #it becomes true because we reach the first character after the whitespaces of the instruction
            Instruction+=element
    if (Instruction[0]=='.'):
        strOfCodePointer=Instruction[Instruction.find('(') + 1:Instruction.find(')')]   #for the address controlling
        if(Instruction[1]=='s'):   #check if its stack part
            if (strOfCodePointer.isdigit()):   #its for the address controlling or it has to use the initialized value
                pointerStack=int(strOfCodePointer)
            count=pointerStack
            startStack=pointerStack
            for i in range (32):    #this part will change all the 0 to 32 byte of that part of memory from XX to MM
                microcontroller[count]="MM"
                count+=1
            stackFlag=True
            dataFlag=False
            codeFlag=False
        elif(Instruction[1]=='d'):
            if (strOfCodePointer.isdigit()):
                pointerData=int(strOfCodePointer)
            count=pointerData
            startData=pointerData
            for i in range (32):
                microcontroller[count]="MM"
                count+=1
            stackFlag=False
            dataFlag=True
            codeFlag=False
        elif(Instruction[1]=='c'):
            if (strOfCodePointer.isdigit()):
                pointerCode=int(strOfCodePointer)
            count=pointerCode
            startCode=pointerCode
            for i in range (32):
                microcontroller[count]="MM"
                count+=1
            stackFlag=False
            dataFlag=False
            codeFlag=True
    elif(Instruction[len(Instruction)-1]==':'): #this if statement check if the instruction is a label definition
        for element in labels: #this loop checks if the label is in the labels list or not(for the backward and forward jump)
            if Instruction[:len(Instruction)-1] == element:
                labels.remove(Instruction[:len(Instruction)-1]) #if it was a backward jump it will remove the element from the list
                flag=True 
        if flag== True:
            for i in range(0,len(FinalOPcode)): #this for loop is because of replacing the new opcode of the backward jumo with the one that has been defind
                if FinalOPcode[i] == ("eb"+Instruction[0:len(Instruction)-1]): #it will search for the opcode of that label in the final opcode list
                    for j in range(i+1,len(FinalOPcode)):
                        counter+=len(FinalOPcode[j])//2  #this part is for adding the number of byte of the instructions
                    FinalOPcode[i] = "eb" + "{:02x}".format(int('00', 16) + counter)
                    opcodeChange = [FinalOPcode[i][k:k+2] for k in range(0, len(FinalOPcode[i]), 2)]  #this part will reverses the string of the opcode to add to the data part in little endian way
                    opcodeChange = opcodeChange[::-1]
                    OPcode2 = ''.join(opcodeChange)
                    strr=""
                    counterLoop=0
                    for k in (OPcode2): #to add the opcode to the code part
                        strr+=k
                        if (counterLoop %2 != 0):
                            microcontroller[pointerCode]=strr
                            strr=""
                            pointerCode+=1
                        counterLoop+=1
                    microcontroller[pointerData]=Instruction[:len(Instruction)-1]+'#'+FinalOPcode[i][2:] #will add the label to the data part with its offset
                    pointerData+=1
                    counter=0 
        labels.append(Instruction[:len(Instruction)-1]) #if the label wasnt available it will append it to the labels list
        LabelFlag=True #this label used because the instruction is a label and it has to count the number of instruction between it
        flag=False
    else:
        if (dataFlag == True ):
            name=""    #this part will seprate the name of the variable and its type 
            typeName=""
            spilitedIns=Instruction.split()  #seprate the instruction with ' ' (space)
            name=spilitedIns[0]
            typeName=spilitedIns[1].upper()   #change all the alphabet of type to upper case
            if typeName == "DWORD":  #dword will take 4 part of the data segment
                for i in range (4):
                    microcontroller[pointerData]= name
                    pointerData+=1
            elif typeName == "WORD": #word will take 2 part of data segment
                for i in range (2):
                    microcontroller[pointerData]= name
                    pointerData+=1
            elif typeName == "BYTE":#byte will take 1 part of data segment
                    microcontroller[pointerData]= name
                    pointerData+=1
        if (codeFlag == True ):
            command="" #to store the command 
            reg1="" #to hold the first register or memory
            reg2="" #to hold the second register or memory
            flagCommand=True 
            flagReg1=False
            flagReg2=False
            for element in Instruction: #to seperate the command and register or memory from the instruction 
                if element==' ' and flagCommand==True:
                    flagCommand=False 
                    flagReg1=True
                elif flagReg1==True and element==',':
                    flagReg1=False
                    flagReg2=True
                elif element!=' ':
                    if flagCommand==True:
                        command+=element
                    elif flagReg1==True:
                        reg1+=element
                    elif flagReg2==True:
                        reg2+=element
            def REG(reg): #for the code of each register
                if(reg=='al' or reg=='ax' or reg=='eax'):
                    return '000'
                elif(reg=='cl' or reg=='cx' or reg=='ecx'):
                    return '001'
                elif(reg=='dl' or reg=='dx' or reg=='edx'):
                    return '010'
                elif(reg=='bl' or reg=='bx' or reg=='ebx'):
                    return '011'
                elif(reg=='ah' or reg=='sp' or reg=='esp'):
                    return '100'
                elif(reg=='ch' or reg=='bp' or reg=='ebp'):
                    return '101'
                elif(reg=='dh' or reg=='si' or reg=='esi'):
                    return '110'
                elif(reg=='bh' or reg=='di' or reg=='edi'):
                    return '111'
                else:
                    return '0'
            def jump(counter , label): #function for the jump instruction
                flagAvailable=False # if the flag have been available which means its a backward jump
                for element in labels:
                    if element == label:
                        labels.remove(label)# if the label is available in the list of labels it will remove it because drive to it
                        flagAvailable=True 
                if flagAvailable==False: # if the label isnt available it will append it to the list
                    labels.append(label)
                    return "eb"+label
                elif flagAvailable==True: #calculate the opcode of the jump
                        finalNum = hex(int('fe', 16) - counter)[2:]
                        return "eb"+finalNum
            def Command(command,reg): #retuen the opcode of the instruction
                if command =='jmp':
                    return jump(counterLabel , reg1)
                elif command =='add':
                    return "000000"
                elif command =='sub':
                    return "001010"
                elif command == 'and':
                    return "001000"
                elif command == 'or':
                    return "000010"
                elif command=='xor':
                    return "001100"
                if command=='inc':#because each register for the inc command has a specific opcode we seprate the registers
                    if reg in Reg8: # to handel the 8_bit register
                        for j in range(len(Reg8)):
                            if reg == Reg8[j]:
                                return 'fec'+str(j)
                    elif reg=='ax' or reg=='eax':
                        return '40'
                    elif reg=='cx' or reg=='ecx':
                        return '41'
                    elif reg=='dx' or reg=='edx':
                        return '42'
                    elif reg=='bx' or reg=='ebx':
                        return '43'
                    elif reg=='sp' or reg=='esp':
                        return '44'
                    elif reg=='bp' or reg=='ebp':
                        return '45'
                    elif reg=='si' or reg=='esi':
                        return '46'
                    elif reg=='di' or reg=='edi':
                        return '47'
                    else:
                        return '0'
                elif command=='dec': #same as the inc 
                    if reg in Reg8: # to handel 8_bit register
                        for j in range(len(Reg8)):
                            if reg == Reg8[j]:
                                index=hex(j+8)[2:]
                                return 'fec'+str(index)
                    elif reg=='ax' or reg=='eax':
                        return '48'
                    elif reg=='cx' or reg=='ecx':
                        return '49'
                    elif reg=='dx' or reg=='edx':
                        return '4a'
                    elif reg=='bx' or reg=='ebx':
                        return '4b'
                    elif reg=='sp' or reg=='esp':
                        return '4c'
                    elif reg=='bp' or reg=='ebp':
                        return '4d'
                    elif reg=='si' or reg=='esi':
                        return '4e'
                    elif reg=='di' or reg=='edi':
                        return '4f'
                    else:
                        return '0'
                elif command=='push':#same as inc
                    if reg=='ax' or reg=='eax':
                        return '50'
                    elif reg=='cx' or reg=='ecx':
                        return '51'
                    elif reg=='dx' or reg=='edx':
                        return '52'
                    elif reg=='bx' or reg=='ebx':
                        return '53'
                    elif reg=='sp' or reg=='esp':
                        return '54'
                    elif reg=='bp' or reg=='ebp':
                        return '55'
                    elif reg=='si' or reg=='esi':
                        return '56'
                    elif reg=='di' or reg=='edi':
                        return '57'
                    elif (int(reg))>=0and (int(reg))<=127: #for the 8-bit imm
                        return '6a' + hex(int(reg))[2:].zfill(2)
                    elif (int(reg))<0 and (int(reg))>= -128: #for the 8-bit imm
                        return '6a' + hex((1 << 8) + int(reg))[2:].zfill(2)
                    elif (int(reg))>=-32768 and (int(reg))<-128:
                        string = "{:x}".format(int(reg))
                        reversedstring = ''.join([string[i:i+2] for i in range(0, len(string), 2)][::-1])
                        return '68'+reversedstring+'0000'
                    elif (int(reg))<=32767 and (int(reg))>127:
                        string = "{:x}".format(int(reg))
                        reversedstring = ''.join([string[i:i+2] for i in range(0, len(string), 2)][::-1])
                        return '68'+reversedstring+'0000'
                        hex_string = "{:x}".format(int(reg)) 
                elif command=='pop': #same as inc
                    if reg=='ax' or reg=='eax':
                        return '58'
                    elif reg=='cx' or reg=='ecx':
                        return '59'
                    elif reg=='dx' or reg=='edx':
                        return '5a'
                    elif reg=='bx' or reg=='ebx':
                        return '5b'
                    elif reg=='sp' or reg=='esp':
                        return '5c'
                    elif reg=='bp' or reg=='ebp':
                        return '5d'
                    elif reg=='si' or reg=='esi':
                        return '5e'
                    elif reg=='di' or reg=='edi':
                        return '5f'
                    else:
                        return '0'
            OPcode=""
            flagCommand=False
            command=command.lower()#i will make all the elements of the instruction to lowercase
            if command!='jmp': #if the command is not jmp it will the registers the lowercase
                reg1=reg1.lower()
                reg2=reg2.lower()
            if command=='inc' or command=='dec' or command=='push' or command=='pop' or command == 'jmp':
                flagCommand=True
            if reg1 in Reg16  or reg2 in Reg16:
                if flagCommand==False:
                    OPcode+='01100110' #prefix byte for 16 bit
                else:
                    OPcode+='66' #prefix byte for 16bit for the push pop inc dec             
            OPcode+=Command(command,reg1) #return the opcode of the command
            if(command=='jmp' and len(labels)==0): #it will change the counterLabel and LabelFlag if there is a forward jump 
                counterLabel=0
                LabelFlag=False
                indirect=False #this flag is for indirect addressing
            if (command == 'jmp' and not reg1 in labels):
                microcontroller[pointerData]=reg1+'#'+OPcode[2:]
                pointerData+=1
            if flagCommand==False: #if the command is not between the pop , push , inc , dec , jmp
                if reg1 in Reg8:
                    if reg2[0]=='[':
                        indirect=True
                        OPcode+="10"
                        s=0
                        d=1
                    else:
                        OPcode+="00"
                        s=0
                        d=0
                elif reg2 in Reg8:
                    if reg1[0]=='[':
                        indirect=True
                        OPcode+="00"
                        s=0
                        d=0
                    else:
                        OPcode+="10"
                        s=0
                        d=1
                else:
                    if reg2[0]=='[':
                        indirect=True
                        OPcode+="11"
                        d=1
                        s=1
                    else:
                        OPcode+="01"
                        d=0
                        s=1
                #MOD_REG_RM
                Reg=""
                RM=""
                MOD_Reg_RM=""
                if reg1[0]=='[' or reg2[0]=='[' :#this will choose the type of mod
                    MOD_Reg_RM='00'  #if its a indirect addressing
                else:
                    MOD_Reg_RM='11'  #if its a register addressing
                if d==0: # this part will choose which part is the RM and which is the REG part to find the opcode
                    for i in reg1:
                        if i!='[':
                            if(i==',' or i==']'):
                                break
                            RM+=i
                    for i in reg2:
                        if i!='[':
                            if(i==',' or i==']'):
                                break
                            Reg+=i
                    if Reg == '0' or RM == '0':
                        OPcode = '0'
                    if indirect == True and not RM in Reg32: #checks if the indirect addressing is true and its a 32 bit register
                        OPcode = '0'
                    elif indirect == False :
                        if RM  in Reg32 and  Reg  in Reg32: #check if both are reg 32
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        elif  RM in Reg16 and  Reg in Reg16: #check if both are reg 16
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        elif  RM in Reg8 and  Reg in Reg8: #check if both are reg 8
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        else:
                            OPcode='0'
                elif d==1:
                    for i in reg1:
                        if i!='[':
                            if(i==',' or i==']'):
                                break
                            Reg+=i
                    for i in reg2:
                        if i!='[':
                            if(i==',' or i==']'):
                                break
                            RM+=i
                    if Reg == '0' or RM == '0':
                        OPcode = '0'
                    if indirect == True and not RM in Reg32:
                        OPcode = '0'
                    elif indirect == False :
                        if RM  in Reg32 and  Reg  in Reg32:
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        elif  RM in Reg16 and  Reg in Reg16:
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        elif  RM in Reg8 and  Reg in Reg8:
                            OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
                        else:
                            OPcode='0'
                    else:
                        OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
            if OPcode=='0': #if the register that is entered isnt a register 
                print("somethind wrong")
                break
            if (command != 'push' and command != 'pop' and command != 'dec' and command != 'inc' and command != 'jmp'):
                #this if checks if the command is in the items above because the opcode is in the hex base it will not enter this if
                instructionCode=int(OPcode,2)
                OPcode=format(instructionCode,'04x') #change the opcode to the format of hex number
            if (LabelFlag==True):
                counterLabel+=len(OPcode)//2
            if (command != 'jmp' or not reg1 in labels ):
                counterLoop=0
                strr=""
                opcodeChange = [OPcode[i:i+2] for i in range(0, len(OPcode), 2)]
                opcodeChange = opcodeChange[::-1]
                OPcode2 = ''.join(opcodeChange)
                for i in (OPcode2):
                    strr+=i
                    if (counterLoop %2 != 0):
                        microcontroller[pointerCode]=strr
                        strr=""
                        pointerCode+=1
                    counterLoop+=1
            if (command == 'push'):  #if we push a 32 reg or 16 or 8 bit reg they will tske number of part of the stack segment
                if ( reg1 in Reg32 ):
                    microcontroller[pointerStack]=microcontroller[pointerStack+1]=microcontroller[pointerStack+2]=microcontroller[pointerStack+3]=reg1
                    pointerStack+=4
                elif (reg1 in Reg16 ):
                    microcontroller[pointerStack]=microcontroller[pointerStack+1]=reg1
                    pointerStack+=4
                elif (reg1 in Reg8 ):
                    microcontroller[pointerStack]=reg1
                    pointerStack+=4
                elif (int(reg1) >=-128 and int(reg1)<=127): #for the 8-bit number
                    microcontroller[pointerStack]=reg1
                    pointerStack+=4
                elif (int(reg1) >=-32768 and int(reg1)<=32767): #for 16-bit number
                    microcontroller[pointerStack]=microcontroller[pointerStack+1]=reg1
                    pointerStack+=4
            elif (command == 'pop') :  #handel the pop of 32-bit reg
                if (reg1 in Reg32):
                    microcontroller[pointerStack-1]=microcontroller[pointerStack-2]=microcontroller[pointerStack-3]=microcontroller[pointerStack-4]='MM'
                    pointerStack-=4
            if (pointerCode %2 !=0):  #if the pointer wasnt point to a part with an even num if it wasnt is has to add 1 to become even align
                pointerCode+=1
            FinalOPcode.append(OPcode)
            # add the final opcode of each instruction to the instruction list
final=""
counter=0 #the counter for the addresses in the memory
if(num != 2 and num!=3 and num != 1 and OPcode=='0'):
    print("invalid input")
elif (num == 2 or num == 1):
    for i in range (256):#to print the memory
        if (i == startCode):
            finalCode='CS '+str(i) + ' : ' +microcontroller[i]
        elif (i == startData):
            finalCode='DS '+str(i) + ' : ' +microcontroller[i]
        elif (i == startStack):
            finalCode='SS '+str(i) + ' : ' +microcontroller[i]
        else:
            finalCode='  '+str(i) + ' : ' +microcontroller[i]
        print (finalCode)
        print ('.........')