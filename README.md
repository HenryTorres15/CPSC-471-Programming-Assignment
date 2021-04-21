# CPSC-471-Programming-Assignment
## Group Members:
Henry Torres - htorres15@csu.fullerton.edu

Armon Rahimi - armon16@csu.fullerton.edu

Jared Schneider - JaredPSchneider@csu.fullerton.edu

Jonathan Story - jstory@csu.fullerton.edu
## Programming Language:
Python 3.9 or higher
## How to execute program:
1. Check Python version is up to date 3.9 or higher, using "py --version" in terminal
2. Open terminal and run the server that will listen for connections
3. Run the server.py program in terminal, "py server.py **PORT**". Example: "py server.py 12000"
4. Open a 2nd terminal and run the client.py program, "py client.py **SERVER-MACHINE** **PORT**". Example: "py client.py 127.0.0.1 12000"
5. From there you will have a list of commands for the client.py
    -ftp> get **FILE NAME**  (downloads file **FILE NAME** from the server)
    -ftp> put **FILE NAME**  (uploads file **FILE NAME** to the server)
    -ftp> ls                 (lists files on the server)
    -ftp> quit               (disconnects from the server and exits)
## Extra notes:
The cliData folder is where all the client files are stored and read. While, the servData folder is where all the server files are stored and read. We also added 3 testing files already included in the servData but you can create new files and test it out for yourself. 