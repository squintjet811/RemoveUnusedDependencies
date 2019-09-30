import re
import subprocess
import pdb
import os
from tqdm import tqdm
from subprocess import DEVNULL


class RmDep:
    """
    This is the class for removing unnecessary dependenceis and build the project by unit compling
    """

    def __init__(self):
        # initialize the data
        self.file_path = None      # the path of the source file
        self.file_content = None   # the original content of the source file
        self.target_line_content = []    #all selected line content
        self.target_line_index = []      #all selected line position in the source file
        self.unnecessary_line_content = []  #unnecessary line content
        self.unnecessary_line_index = []    #unnecessary line position in the source file
        self.cur_line_num = 0               #the line indicater during the scan
        self.pattern = re.compile(r'#include')    #regex pattern to search
        self.idx = 0  #index for tracking the progress of execution

    def set_file_path(self, file_path):
        """
        Set the file path for any type of .cpp or .h file to check dependencies
        :param file_path: string type which contains the absolute path of the file
        :return: None
        """

        self.file_path = file_path  # set the file path

    def scan_line(self):
        """
         Open the file and scan for all hash includes
        :return: None
        """
        # scan the file give the full path of the file
        with open(self.file_path, 'r') as file_pointer:
            self.cur_line_num = 0
            self.file_content = file_pointer.readlines()

        for string_line in self.file_content:

            # if the hash include line is found
            if self.pattern.match(string_line):
                self.target_line_index.append(self.cur_line_num)
                self.target_line_content.append(string_line)

            self.cur_line_num += 1

    def remove_selected_line(self):
        """
        remove one line at a time
        :return: None
        """
        line_num = self.target_line_index[self.idx]
        line_content = self.target_line_content[self.idx]
        # delete the line
        with open(self.file_path, 'w+') as file_pointer:
            for i, line in enumerate(self.file_content, 0):
                #print(i, line_num)
                #print(line)
                if i != line_num:
                    #print("write")
                    file_pointer.write(line)

        #print(line_num)
        #print(line_content)

    def compile(self):
        """
        compile the file
        :return: None
        """
        result = subprocess.Popen("bash run.sh", shell=True, stdout=DEVNULL, stderr=subprocess.PIPE)
        text = result.communicate()[0]
        return_code = result.returncode

        print("return code part is  : ", return_code)

        if return_code == 0:

            self.unnecessary_line_index.append(self.idx)
            self.unnecessary_line_content.append(self.target_line_content[self.idx])

    def reset_file(self):
        """
        reset the file back to its original content
        :return: None

        """
        with open(self.file_path, 'w+') as file_pointer:
            for line in self.file_content:
                file_pointer.write(line)
        print("Reset the file to source")

    def run(self):
        """
        execute the bulk function body
        :return: None
        """
        self.scan_line()
        for self.idx in tqdm(range(len(self.target_line_index))):
            self.remove_selected_line()
            self.compile()
            self.reset_file()
        print("The unnecessary lines are: ")
        print(self.unnecessary_line_content)

def main():

    file_name = "./src/jhumark1/source/robot/robotTask.cpp"

    rm_dep = RmDep()
    rm_dep.set_file_path(file_name)
    rm_dep.run()

    return 0


if __name__ == "__main__":
    main()
