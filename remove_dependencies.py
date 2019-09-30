import re
import subprocess
import pdb
import os
from tqdm import tqdm
from subprocess import DEVNULL,STDOUT, check_call



def main():
    file_name = "./src/jhumark1/source/robot/robotTask.h"
    #file_name =  "./src/rmdep/src/test1.cpp"
    re_pattern = re.compile(r'#include')

    target_line_content = []
    target_line_index = []
    unnecessary_line_content = []
    unnecessary_line_index = []
    with open(file_name, 'r') as file_pointer:
        line_num = 0;
        target_line = file_pointer.readlines()
    for string_line in target_line:

        #if the hashinclude line is found
        if re_pattern.match(string_line):
            target_line_index.append(line_num)
            target_line_content.append(string_line)

        line_num += 1

    print("Scanning file complete------------")
    print("hash include places")
    print(target_line_content)
    #pdb.set_trace()

    for idx in tqdm(range(len(target_line_index))):
        line_num = target_line_index[idx]
        line_content = target_line_content[idx]
        #delete the line
        with open(file_name, 'w+') as file_pointer:
            for i, line in enumerate(target_line, 0):
                #print(i, line_num)
                #print(line)
                if i != line_num:
                    file_pointer.write(line)

        print(line_num)
        print(line_content)
        print("pause")
        #pdb.set_trace()

        #test the compile
        result = subprocess.Popen("bash run.sh", shell = True, stdout= DEVNULL, stderr = subprocess.PIPE)
        text = result.communicate()[0]
        return_code = result.returncode
        print("text part is  : ", text)
        print("return code part is  : ", return_code)
        print("removed line is : ", line_content)
        if(return_code == 0):

            unnecessary_line_index.append(i)
            unnecessary_line_content.append(line_content)

        #place the line back
        with open(file_name, 'w+') as file_pointer:
            for i, line in enumerate(target_line, 0):
                if i != line_num:
                    file_pointer.write(line)
                else:
                    file_pointer.write(line_content)
                    file_pointer.write(line)

        #pdb.set_trace()
    print("unnecessary line in builds are", unnecessary_line_content)
    #add the part to replace the file to the original
    with open(file_name, 'w+') as file_pointer:
        for line in target_line:
            file_pointer.write(line)
    print("Reset the file to source")    


    return 0



if __name__ == "__main__" :
    main()
