FinalOPcode=[] #holding the final opcode of all instructions
labels=[]      #a list of labels 
instructions=[] #a list of instructions 
counterLabel=0 #to count the number of each instructions that is assembled between the definition of the label and jump to that label(for the backeard jump)
LabelFlag=False #it uses for the forward jump
flag=False #for the backward jump if the label was available
counter=0 #it's the counter of instruction for the forward jump
print("Which way you want to read data from:1-file 2-CommandLine..... or 3-Exit")
num=int(input()) 
if num == 1: #if the input should be read from a file
    path=input("Enter the path of the file: ") #get the path of the file and hold it in the path
    with open(path, "r") as file: #read the file
        instructions = file.readlines()  #hold each line a part as a string in instructions list
elif (num == 2): #if instructions should be read from the command line and store it in instructions list
    while(1):
        Instruction=input("Enter the instruction you want to assemble(if there is no instruction to assemble just press enter): ")
        if (not Instruction): #if there was no line or instructions as input (or enter) it will break the while loop
            break
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
    if(Instruction[len(Instruction)-1]==':'): #this if statement check if the instruction is a label definition
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
                    counter=0 
        labels.append(Instruction[:len(Instruction)-1]) #if the label wasnt available it will append it to the labels list
        LabelFlag=True #this label used because the instruction is a label and it has to count the number of instruction between it
        flag=False
    else:
        command=""
        reg1=""
        reg2=""
        flagCommand=True
        flagReg1=False
        flagReg2=False
        for element in Instruction:
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
        def REG(reg):
            if(reg=='al' or reg=='ax' or reg=='eax'):
                return '000'
            if(reg=='cl' or reg=='cx' or reg=='ecx'):
                return '001'
            if(reg=='dl' or reg=='dx' or reg=='edx'):
                return '010'
            if(reg=='bl' or reg=='bx' or reg=='ebx'):
                return '011'
            if(reg=='ah' or reg=='sp' or reg=='esp'):
                return '100'
            if(reg=='ch' or reg=='bp' or reg=='ebp'):
                return '101'
            if(reg=='dh' or reg=='si' or reg=='esi'):
                return '110'
            if(reg=='bh' or reg=='di' or reg=='edi'):
                return '111'
        def jump(counter , label):
            flagAvailable=False
            for element in labels:
                if element == label:
                    labels.remove(label)
                    flagAvailable=True
            if flagAvailable==False:
                labels.append(label)
                return "eb"+label
            elif flagAvailable==True:
                    finalNum = hex(int('fe', 16) - counter)[2:]
                    return "eb"+finalNum
        def Command(command,reg):
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
            if command=='inc':
                if reg=='ax' or reg=='eax':
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
            elif command=='dec':
                if reg=='ax' or reg=='eax':
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
            elif command=='push':
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
                elif (int(reg))>=0and (int(reg))<=127:
                    return '6a'+hex(int(reg))[2:]
                elif (int(reg))<0 and (int(reg))>= -128:
                    return '6a'+hex(int(reg))[3:]
            elif command=='pop':
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
        OPcode=""
        flagCommand=False
        command=command.lower()
        if command!='jmp':
            reg1=reg1.lower()
            reg2=reg2.lower()
        if command=='inc' or command=='dec' or command=='push' or command=='pop' or command == 'jmp':
            flagCommand=True
        if reg1=='ax' or reg1=='cx' or reg1=='dx' or reg1=='bx' or reg1=='sp' or reg1=='bp' or reg1=='si' or reg1=='di':
            if flagCommand==False:
                OPcode+='01100110'
            else:
                OPcode+='66'
        OPcode+=Command(command,reg1)
        if(command=='jmp' and len(labels)==0):
            counterLabel=0
            LabelFlag=False
        if flagCommand==False:
            if reg1=='al'or reg1=='bl' or reg1=='cl'or reg1=='dl'or reg1=='ah' or reg1=='bh' or reg1=='ch'or reg1=='dh':
                if reg1[0]=='[':
                    OPcode+="10"
                    d=1
                    s=0
                else:
                    OPcode+="00"
                    s=0
                    d=0
            else:
                if reg2[0]=='[':
                    OPcode+="11"
                    d=1
                    s=1
                else:
                    OPcode+="01"
                    d=0
                    s=1
            Reg=""
            RM=""
            MOD_Reg_RM=""
            if reg1[0]=='[' or reg2[0]=='[' :
                MOD_Reg_RM='00'
            else:
                MOD_Reg_RM='11'
            if d==0:
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
                OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
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
                OPcode+=MOD_Reg_RM+REG(Reg)+REG(RM)
        if (command != 'push' and command != 'pop' and command != 'dec' and command != 'inc' and command != 'jmp'):
            instructionCode=int(OPcode,2)
            OPcode=format(instructionCode,'04x')
        if (LabelFlag==True):
            counterLabel+=len(OPcode)//2
        FinalOPcode.append(OPcode)
final=""
counter=0
if(num != 2 and num!=3 and num != 1):
    print("invalid input")
elif (num == 2 or num == 1):
    for i in range(0,len(FinalOPcode)):
        final+='0x'+'0'*(16-len(str(counter)))+str(counter)+': '+FinalOPcode[i]
        counter+=len(FinalOPcode[i])//2
        print(final)
        final=""