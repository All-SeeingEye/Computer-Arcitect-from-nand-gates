import sys
weight = {'R0':'0',
              'R1':'1',
              'R2':'2',
              'R3':'3',
              'R4':'4',
              'R5':'5',
              'R6':'6',
              'R7':'7',
              'R8':'8',
              'R9':'9',
              'R10':'10',
              'R11':'11',
              'R12':'12',
              'R13':'13',
              'R14':'14',
              'R15':'15',
              'SP':'0',
              'LCL':'1',
              'ARG':'2',
              'THIS':'3',
              'THAT':'4',
              'SCREEN':'16384',
              'KBD':'24576'}

c_bits = {'0':'0101010',
          '1':'0111111',
          '-1':'0111010',
          'D':'0001100',
          'A':'0110000',
          'M':'1110000',
          '!D':'001101',
          '!A':'0110001',
          '!M':'1110001',
          '-D':'0001111',
          '-A':'0110011',
          '-M':'1110011',
          'D+1':'0011111',
          'A+1':'0110111',
          'M+1':'1110111',
          'D-1':'0001110',
          'A-1':'0110010',
          'M-1':'1110010',
          'D+A':'0000010',
          'D+M':'1000010',
          'D-A':'0010011',
          'D-M':'1010011',
          'A-D':'0000111',
          'M-D':'1000111',
          'D&A':'0000000',
          'D&M':'1000000',
          'D|A':'0010101',
          'D|M':'1010101'}

d_bits = {'null':'000',
          'M':'001',
          'D':'010',
          'MD':'011',
          'A':'100',
          'AM':'101',
          'AD':'110',
          'AMD':'111'}

j_bits = {'JGT':'001',
          'JEQ':'010',
          'JGE':'011',
          'JLT':'100',
          'JNE':'101',
          'JLE':'110',
          'JMP':'111'}



def parser(input_file:str):
    ls=[]
    i = 0
    # read the file
    with open(input_file,'r') as f:
        lines = f.read().splitlines()
    # remove the comments
    lines = [item.split('//')[0].strip() for item in lines]
    lines = [line for line in lines if not line.startswith('//')]
    lines = [line for line in lines if line!='']
    # Handle the lables
    # The adress of the lables is the index of the next instruction ignoring the indexes of the labels.
    for line in lines:
        if line.startswith('(') and line.endswith(')'):
            ls.append(line.strip('()'))
        else:
            ls.append(str(i))
            i += 1
    # In case of consecutive indexes
    i = 0
    while i < len(ls) - 1:
        if not ls[i].isdigit():
            j = i + 1
            while j < len(ls):
                if ls[j].isdigit():
                    weight[ls[i]] = ls[j]
                    break
                j += 1
            if j == len(ls):
                weight[ls[i]] = None  # Set value as None if no numeric value found to the right
        i += 1
    
    lines = [line for line in lines if not line.startswith('(')]
    return lines,weight


def assemble(codelines:list,weight:dict):
    ls = []
    i=0
    for line in codelines:
        if line.startswith('@'):
            line = line.replace('@','')
            if line.isdigit():
                line = bin(int(line))[2:]
                ls.append(str(line).zfill(16))
            else:
                try:
                    line = bin(int(weight[line]))[2:]
                    ls.append(str(line).zfill(16))
                except KeyError:
                    weight[line] = str(16+i)
                    i=i+1
                    line = bin(int(weight[line]))[2:]
                    ls.append(str(line).zfill(16))


        else:
            if ';' not in line:
                dest,comp = line.split('=')

                destination = d_bits[dest]
                computue = c_bits[comp]

                binary_code = '111'+computue+destination+'000'  
                ls.append(binary_code)            
            else:
                dest_comp,jmp = line.split(';')
                try:
                    dest,comp = dest_comp.split('=')
                except ValueError:
                    comp = dest_comp
                    dest = 'null'

                destination = d_bits[dest]
                computue = c_bits[comp]
                jump = j_bits[jmp]

                binary_code = '111'+computue+destination+jump  
                ls.append(binary_code)           

    
    return ls

def output_file(input_file:str,machine_code:list):
    output_file = input_file.replace('.asm','.hack')
    with open(output_file,'w') as f:
        for line in machine_code:
            f.write(line + '\n')


if __name__ == "__main__":
    input_file = sys.argv[1]
    asmcode,weights = parser(input_file)
    machine_code = assemble(asmcode,weights)
    output_file(input_file,machine_code)


