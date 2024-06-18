
import subprocess
import webbrowser
import pymysql
import sys
import os

# new languages detils are store in the class
# every time the interepter encoters the new file creation for write and append, for both different objects are creates
# with same name.
class lang_details:
    def __init__(self):
        self.language_type = ""
        self.file_name = ""
        self.append_mode = False

    def update_details(self, content):
        '''the details of the file is gathered and update this for all languages taht are available'''
        list = content.split(" ")
        i=0
        while i < len(list):
            if list[i] == "<python":
                self.language_type = "python"
            elif list[i] == "<html":
                self.language_type = "html"
            elif list[i] == "<java":
                self.language_type = "java"
            elif list[i] == "name":
                self.file_name = list[list.index("name") + 2]
            elif list[i] == "append" and list[i+2] == "true":
                self.append_mode = True
            i+=1

# now we create a class as seperate module for handling the mysql commands and executint them
class mysql_execution:          # read note 2
    def __init__(self):
        self.hostname = "localhost"
        self.user = "root"
        self.password = ""
        self.database = ""
        self.file_name = ""
        self.language_type="mysql"
        self.append_mode = False

    def update_details(self,lines):
        list = lines.split(" ")
        i=0
        while i<len(list):
            if list[i] == "name":
                self.file_name = list[i+2]
            elif list[i] == "hostname":
                self.hostname = list[i+2]
            elif list[i] == "user":
                self.user = list[i+2]
            elif list[i] == "password":
                self.password = list[i+2]
            elif list[i] == "database":
                self.database = list[i+2]
            i = i+1

    def sql_connection(self,file):
        file.write("import pymysql\n")
        file.write(f"connection = pymysql.connect(host = '{self.hostname}', user = '{self.user}', password = '{self.password}')\n")
        print("The connection object:")
        file.write("print(connection)\n")
        file.write("cursor = connection.cursor()\n")
        if self.database != "":
            file.write(f"cursor.execute('use {self.database}')\n")


'''this function used to write the contents into the file with file pointer and content '''
def script_write(file, content):
    file.write(content)

# writing lines of dtabase command into a seperate python file
def database_write(file, content):
    if "create" in content:
        file.write(f"cursor.execute('{content[:-1]}')\nconnection.commit()\n")
        print("create command is executed")
    elif "use" in content:
        file.write(f"cursor.execute('{content[:-1]}')\nconnection.commit()\n")
        print("database is changed")
    elif "select" in content:
        file.write(f"cursor.execute('{content[:-1]}')\nresult = cursor.fetchall()\nprint('Data from the table')\n")
        file.write("for row in result:\n    print(row)\n")
        print("select command is written")
    else:
        file.write(f"cursor.execute('{content[:-1]}')\nconnection.commit()\n")


# main code:

lang_pointer = []       # class pointer are stored
lang_file_name = {}     # languages file name specified by the user in stored
file_open_pointer = []  # currently opend files pointer are stored -- helpful for nested files type
mode = 0                # used to say whether the contents are writtable
open_close = 0          # to restrict the write operation of the statements that contaion open and close statemetns
database_pointer = 0    # this pointer is used to write the database command into the pyhton file because
                            # mysql database requires different type of writting into the python file
'''
mode=1 --python
'''


with open("./text_files/script2","r") as script_file:
    for lines in script_file:   # reading the script file

        # evaluating the code related to python
        if "<python" in lines:      # openning the file and appending to respective lists
            open_close = 1
            lang_pointer.append(lang_details())     # object of lang_detils is created and stored
            lang_pointer[-1].update_details(lines)  # calling the update function to update the info
            filename = lang_pointer[-1].file_name   # coping the file name from the object
            lang_file_name[filename] = "python"  # current

            if lang_pointer[-1].append_mode:        # appending contents to existing files
                python = open(f"./text_files/{filename}","a")
            else:                                   # writing to the files
                python = open(f"./text_files/{filename}","w")
            mode += 1                               # increment help-s in nested script writing
            file_open_pointer.append(python)        # appending to list that contains current file pointer opened

        elif "</python" in lines:                   # closing the opend file
            open_close = 1
            mode -= 1
            file_open_pointer[-1].close()           # closing the python file
            file_open_pointer.pop()                 # deleting the pointer

        elif "<pyhtml" in lines:
            open_close = 1
            lang_pointer.append(lang_details())
            lang_pointer[-1].update_details(lines)
            lang_pointer[-1].file_name += ".html"
            filename = lang_pointer[-1].file_name
            lang_file_name[filename] = "html"

            if lang_pointer[-1].append_mode:        # appending contents to existing files
                html = open(f"./text_files/{filename}","a")
            else:                                   # writing to the files
                html = open(f"./text_files/{filename}","w")
            mode += 1                               # increment help-s in nested script writing
            file_open_pointer.append(html)        # appending to list that contains current file pointer opened

        elif "</pyhtml" in lines:
            open_close = 1
            mode -= 1
            file_open_pointer[-1].close()           # closing the python file
            file_open_pointer.pop()                 # deleting the pointer

        elif "<java" in lines:
            open_close = 1
            lang_pointer.append(lang_details())
            lang_pointer[-1].update_details(lines)
            lang_pointer[-1].file_name += ".java"
            filename = lang_pointer[-1].file_name
            lang_file_name[filename] = "java"

            if lang_pointer[-1].append_mode:        # appending contents to existing files
                java = open(f"./text_files/{filename}","a")
            else:                                   # writing to the files
                java = open(f"./text_files/{filename}","w")
            mode += 1                               # increment help-s in nested script writing
            file_open_pointer.append(java)        # appending to list that contains current file pointer opened

        elif "</java" in lines:
            open_close = 1
            mode -= 1
            file_open_pointer[-1].close()           # closing the python file
            file_open_pointer.pop()                 # deleting the pointer

        elif "<mysql" in lines:      # openning the file and appending to respective lists
            open_close = 1
            database_pointer = 1
            lang_pointer.append(mysql_execution())     # object of lang_detils is created and stored
            lang_pointer[-1].update_details(lines)  # calling the update function to update the info
            filename = lang_pointer[-1].file_name
            lang_file_name[filename] = "mysql"  # current

            if lang_pointer[-1].append_mode:        # appending contents to existing files
                mysql = open(f"./text_files/{filename}","a")
            else:                                   # writing to the files
                mysql = open(f"./text_files/{filename}","w")
                lang_pointer[-1].sql_connection(mysql)
            mode += 1                               # increment help-s in nested script writing
            file_open_pointer.append(mysql)        # appending to list that contains current file pointer opened

        elif "</mysql" in lines:
            open_close = 1
            database_pointer = 0
            mode -= 1
            file_open_pointer[-1].close()           # closing the python file
            file_open_pointer.pop()                 # deleting the pointer

        if database_pointer == 1 and open_close!=1:
            open_close = 1
            database_write(file_open_pointer[-1], lines)

        if mode != 0 and open_close!=1:
            script_write(file_open_pointer[-1], lines)

        open_close = 0                              # set to zero to enable the script_write function to write into the file

print(lang_file_name)

# executing the scripts

print("-------------------execution begins----------------------")

keys = list(lang_file_name.keys())
print(keys)

for i in range(len(keys)):
    file_type = lang_file_name[keys[i]]
    script_path = f".\\text_files\\{keys[i]}"
    if(file_type == "python"):
        print("--------python file is identified---------")
        # script_path+=".py"
        try:
            # Run the script as a separate process
            subprocess.run(["python", script_path], check=True)
            print("Script executed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")

    elif (file_type == "html"):
        print("---------HTML file is identified---------")
        webbrowser.open(script_path, new=2)

        # Open the HTML file in the default web browser
        # webbrowser.open("file://" + script_path)
    elif (file_type == "java"):
        print("----------JAVA file is identified---------")

        # Specify the path to your Java file
        java_file_path = f'C:\\Users\\prana\\PycharmProjects\\multilang\\venv\\text_files\\{keys[i]}'

        # Compile the Java file with a destination directory
        compile_command = f'javac -d C:\\Users\\prana\\PycharmProjects\\multilang\\venv\\text_files {java_file_path}'
        subprocess.run(compile_command, shell=True)
        print("Compilation is successful")

        # Change the current working directory
        os.chdir('C:\\Users\\prana\\PycharmProjects\\multilang\\venv\\text_files')

        # Run the compiled Java class file
        class_name = keys[i].split(".")
        class_name = class_name[0]
        run_command = f'java {class_name}'
        subprocess.run(run_command, shell=True)


    elif file_type == "mysql":
        print("--------mysql file is identified---------")
        # script_path+=".py"
        try:
            # Run the script as a separate process
            python_interpreter = sys.executable             # this is different from above read note 1
            subprocess.run([python_interpreter, script_path], check=True)
            print("Script executed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")


'''
notes:
note 1:
    python_interpreter = sys.executable
    this is used because while using the subprocess it could create a seperate environment and hence installed packages
    in the current environment is unavailable to the running process henc eyou get the module not found error, to
    rectify thie issue we pass the current working environment and hence the process executs successfully
    
note 2:
    class mysql_execution
    this class is creared to hanndle the mysql execution because it needs special code writing techniqueu
    seperate class ensures the code validtion for connecting the mysql and python and helps in execution of sql code as
    a python code

to do:
*) define a methadology for defining variables that can be used in multiple languages
*) a good idea is using JSON file for storing the variable and its value as key:value pair
*) else try implementing the shared memory

works completed:
*) successfully executed python, html, java, mysql files inside a single script
*) nested fiels can also be executed easily

wordks to be done:
*) bro you need to develop a protocol :)
*) directory management
*) pipelining for inter process communication
*) error handling mechanism

future enhancement:
*) try implementing all necessary languages
*) modularity
*) IDE for the script file
*) launching as an app

'''
