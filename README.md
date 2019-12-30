# RemoveUnusedDependencies

## Introduction
This is a small python script to find the unused hash includes during the build time of a c++ project.

## Install
Run git clone to clone the current repo to your local directory

## Envirnment/Dependencies
- tpdm == 4.36.1
- python == 3.7

## Run
In your local branch, run the scripts with an additional input of the path of the file you want to test 

```python3 remove_dependencies.py your_cpp_file_path ```

for example:

```python3 remove_dependecies.py hello_world.cpp```

## To Do List
- Add an input option for build command for different compilier
- Add an option to read a cmake file to read a list of file for a project
- Add multi threading to improve the performance 
