import sys
import os
def update_dic_push(index,name):
    return { 
                'constant':[f'@{index}','D=A','@SP' , 'A=M',   'M=D',   '@SP',  'M=M+1'] ,
                'argument': ['@ARG', "D=M",f"@{index}","A=D+A","D=M","@SP","A=M","M=D","@SP","M=M+1"],
                'local' : ["@LCL", "D=M",f"@{index}","A=D+A","D=M","@SP","A=M","M=D","@SP","M=M+1"],
                "this": ["@THIS","D=M",f"@{index}","A=D+A","D=M","@SP","A=M","M=D","@SP","M=M+1"],
                "that": ["@THAT", "D=M",f"@{index}","A=D+A","D=M","@SP","A=M","M=D","@SP","M=M+1"],
                "temp": [f"@R{index + 5}","D=M","@SP","A=M","M=D","@SP", "M=M+1"],
                "pointer": [f"@R{index + 3}","D=M","@SP","A=M","M=D","@SP", "M=M+1"],
                "static": [f"@{name}StaticTest{index}","D=M","@SP","A=M","M=D","@SP", "M=M+1"]
            }

def update_dic_pop(index,name):
    return {
                'argument': ["@ARG","D=M",f"@{index}", "A=D+A","D=A", "@R13", "M=D","@SP", "M=M-1","A=M", "D=M", "@R13", "A=M", "M=D"],
                'local' : ["@LCL", "D=M", f"@{index}", "A=D+A","D=A", "@R13", "M=D","@SP", "M=M-1","A=M", "D=M", "@R13", "A=M", "M=D"],
                "this": ["@THIS", "D=M", f"@{index}",  "A=D+A","D=A", "@R13", "M=D","@SP", "M=M-1","A=M", "D=M", "@R13", "A=M", "M=D"],
                "that":["@THAT", "D=M", f"@{index}",  "A=D+A","D=A", "@R13", "M=D","@SP", "M=M-1","A=M", "D=M", "@R13", "A=M", "M=D"],
                "temp": [f"@R{index + 5}","D=A","@R13","M=D","@SP","M=M-1","A=M","D=M","@R13","A=M","M=D"],
                "pointer": [f"@R{index + 3}","D=A","@R13","M=D","@SP","M=M-1","A=M","D=M","@R13","A=M","M=D"],
                "static": [f"@{name}StaticTest{index}","D=A","@R13","M=D","@SP","M=M-1","A=M","D=M","@R13","A=M","M=D"]
            }

def update_dic_logic(i):
    return {
                'add':["@SP", "M=M-1","A=M", "D=M", "@SP", "M=M-1","@SP","A=M", "M=D+M", "@SP","M=M+1"],
                'sub':["@SP", "M=M-1","A=M", "D=M", "@SP", "M=M-1","@SP","A=M", "M=M-D", "@SP","M=M+1"],

                'and':["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=D&M", "@SP","M=M+1"],
                'or': ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=D|M", "@SP","M=M+1"],

                'neg':["@SP", "AM=M-1", "M=-M",'@SP','M=M+1'],
                'not':["@SP", "AM=M-1", "M=!M",'@SP','M=M+1'],

                'lt': ['@SP','AM=M-1','D=M','@SP','AM=M-1','D=M-D','@LESS_THAN'+str(i),'D;JLT','@SP','A=M','M=0','@END'+str(i),'0;JMP','(LESS_THAN'+str(i)+')','@SP','A=M','M=-1','(END'+str(i)+')','@SP','M=M+1'],
                'gt': ["@SP","AM=M-1", "D=M",  "@SP",  "AM=M-1", "D=M-D", "@GREATER_THAN"+str(i), "D;JGT", "@SP",  "A=M",  "M=0",  "@END"+str(i), "0;JMP", "(GREATER_THAN"+str(i)+')',  "@SP", "A=M","M=-1",  "(END"+str(i)+')',  "@SP", "M=M+1"],
                'eq': ['@SP', 'AM=M-1', 'D=M', '@SP' ,'AM=M-1', 'D=M-D', '@EQUAL'+str(i) ,'D;JEQ', '@SP', 'A=M', 'M=0', '@END'+str(i), '0;JMP', '(EQUAL'+str(i)+')', '@SP', 'A=M', 'M=-1', '(END'+str(i)+')', '@SP', 'M=M+1'],

                'inf_loop':['(LOOP)', '@LOOP', '0;JMP']
            }

def update_dic_branch(text):
    return{
        'label':[f'(${text})'],
        'if-goto': ['@SP','M=M-1','@SP','A=M','D=M',f'@${text}','D;JNE'],
        'goto': [f'@${text}','0;JMP'],
        'function':[f'({text})'],
    }

def update_call(i,text,value,name):
    return { 'call':[   f"@{name}_RETURN_{i}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                        "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                        "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                        "@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                        "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                        "@SP", "D=M", "@5", "D=D-A", f"@{value}", "D=D-A", "@ARG", "M=D",
                        "@SP", "D=M", "@LCL", "M=D", f"@{text}", "0;JMP",
                        f"({name}_RETURN_{i})"
]
    }

dic_return = {'return': [ "@LCL", "D=M", "@R7", "M=D", "@5", "A=D-A", "D=M", "@R14", "M=D", "@ARG", "D=M", "@0", "D=D+A", "@R13", "M=D",
                    "@SP", "M=M-1", "@SP", "A=M", "D=M", "@R13", "A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1", "@R7", "D=M", "@1",
                    "A=D-A", "D=M", "@THAT", "M=D", "@R7", "D=M", "@2", "A=D-A", "D=M", "@THIS", "M=D", "@R7", "D=M", "@3", "A=D-A",
                    "D=M", "@ARG", "M=D", "@R7", "D=M", "@4", "A=D-A", "D=M", "@LCL", "M=D", "@R14", "A=M", "0;JMP"]}

dic_main = {'main':['@0','D=A','@SP','A=M','M=D','@SP','M=M+1']}

def remove_comments(lines):
    lines = [item.split('//')[0].strip() for item in lines]
    lines = [line for line in lines if not line.startswith('//')]
    lines = [line for line in lines if line!='']

    return lines

def translator(para,name):
    
    ls = []
    i = 0
    j = 1
    for line in para:
        ls.append('//   '+line)

        if line.startswith('push') or line.startswith('pop'):
            dxn,segment,value = line.split()
            if dxn == 'push':
                push_segs = update_dic_push(int(value),name)
                ls.extend(push_segs[segment])
            elif dxn == 'pop':
                pop_segs = update_dic_pop(int(value),name)
                ls.extend(pop_segs[segment])
        
        elif line.startswith('label') or line.startswith('if-goto') or line.startswith('goto') or line.startswith('function'):
            if not line.startswith('function'):
                command,text = line.split()
                branch_dic = update_dic_branch(text)
                ls.extend(branch_dic[command])
            else:
                command,text,value = line.split()
                branch_dic = update_dic_branch(text)
                if text == 'Sys.main':
                    ls.extend(branch_dic['function'])
                    for k in range(int(value)):
                        ls.extend(dic_main['main'])
                else:
                    ls.extend(branch_dic[command])

        elif line.startswith('call'):
            command,text,value = line.split()
            call_dic = update_call(j,text,value,name)
            ls.extend(call_dic['call'])
            j = j + 1

        elif line == 'return':
            ls.extend(dic_return['return'])

        else:
            i = i+1
            logical_expr = update_dic_logic(i)
            ls.extend(logical_expr[line])

    return ls
                
def write_asm(input_file,code):
    with open(input_file.split('.')[0] + '.asm','w') as f:
        for line in code:
            f.write(line+'\n')

def write_code_vm(directory):
    input_file = directory
    call0 = []
    with open(input_file,'r') as f:
        para = f.read().splitlines()
        para = remove_comments(para)
        code = translator(para,directory)
        # if input_file == 'Sys.vm':
        #     call_dic = update_call('0','Sys.init','0')
        #     call0.extend(['// BOOTSTRAP START'])
        #     call0.extend(['@256','D=A','@SP','M=D'])
        #     call0.extend(call_dic['call'])
        #     call0.extend(['// BOOTSTRAP END'])
        #     call0.extend(code)
        #     code = call0
        write_asm(directory,code)

def write_code(directory):

    files_lis = os.listdir(directory)
    files = [f for f in files_lis if f.split('.')[1] == 'vm' and f!='Sys.vm']
    vm_files = []
    if 'Sys.vm' not in files_lis:
        vm_files = files
    else:
        vm_files = ['Sys.vm']
        vm_files.extend(files)
    call0 = []

    output_file = directory + '.asm'
    with open(f'{directory}'+ '/' + f'{output_file}','w') as asm_file:
        for file in vm_files:
            with open(f'{directory}'+'/'+f'{file}','r') as vm_file:
                para = vm_file.read().splitlines()
                para = remove_comments(para)
                code = translator(para,file)
                if file == 'Sys.vm':
                    call_dic = update_call('0','Sys.init','0',file)
                    call0.extend(['// BOOTSTRAP START'])
                    call0.extend(['@256','D=A','@SP','M=D'])
                    call0.extend(call_dic['call'])
                    call0.extend(['// BOOTSTRAP END'])
                    call0.extend(code)
                    code = call0
            code = [line + "\n" for line in code]
            asm_file.writelines(code)



if __name__ == "__main__":
    directory = sys.argv[1]
    try:
        directory.split('.')[1]== 'vm'
        write_code_vm(directory)
    except IndexError:
        write_code(directory)








