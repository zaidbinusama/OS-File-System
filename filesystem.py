import os
import threading
import sys

filesInUse = []
root = os.getcwd()
global datdict
datdict = {}


def thread_function(thread_number, arr):

    for a in arr:
        a =a.strip()
        a = a.split(' ')
        if a[0] == 'create':
            createFile(a[1])
        elif a[0] == 'delete':
            deleteFile(a[1])
        elif a[0] == 'makeDir':
            makeDirectory(a[1])
        elif a[0] == 'changeDir':
            changeDirectory(a[1])
        if a[0] == 'open':
            a[1] = a[1].replace("<", "")
            a[1] = a[1].replace(">", "")
            a[1] = a[1].replace("\n", "")
            args = a[1].split(',')
            openFile(args[0], args[1])
        elif a[0] == 'read_from_file':
            a[1] = a[1].replace("<", "")
            a[1] = a[1].replace(">", "")
            a[1] = a[1].replace(",", "")
            a[1] = a[1].replace("\n", "")
            a[2] = a[2].replace(",", "")
            a[3] = a[3].replace("\n", "")
            openFile(a[1], 'x', '', a[2], a[3])
        elif a[0] == 'close':
            a[1] = a[1].replace("<", "")
            a[1] = a[1].replace(">", "")
            a[1] = a[1].replace("\n", "")
            args = a[1].split(',')
            closeFile(args[0])
        elif a[0] == 'write_to_file':
            # a[2] = a[2:-1]
            # print(a[2:])
            a[2] = ' '.join(a[2:])
            a[1] = a[1].replace("<", "")
            a[1] = a[1].replace(">", "")
            a[1] = a[1].replace("\n", "")
            a[1] = a[1].replace(",", "")
            a[2] = a[2].replace(",", "")
            a[2] = a[2].replace("\n", "")
            

            print(a[2])
            openFile(a[1], 'w', a[2])
        elif a[0] == 'write_at':
            a[1] = a[1].replace("<", "")
            a[1] = a[1].replace(">", "")
            a[1] = a[1].replace("\n", "")
            a[1] = a[1].replace(",", "")
            contentu = a[2:-1]
            # a[2] = a[2].replace(",", "")
            a[3] = a[3].replace("\n", "")
            # a[2] = a[2:-1]
            a[3] = a[3].replace(",", "")
            a[4] = a[4].replace("\n", "")
            # print(a)
            contentu = ' '.join(contentu)
            print(contentu)
            openFile(a[1], 'w', contentu, a[-1])        
        elif a[0] == 'truncate_file':
            truncateFile(a[1], a[2])
        elif a[0] == 'mov':
            moveFile(a[1], a[2])

        elif a[0] == 'show':
            showDat()
        elif a[0] == 'exit':
            sys.exit(0)


def showDat():
    readDat()
    for key in datdict:
        print(key, datdict[key])


def saveDat():
    file = open(root+"/" + "dat.dat", "w")
    for key in datdict:
        file.write(key + "#" + datdict[key] + "\n")
    file.close()


def writeDat(filename):
    readDat()
    file = open(filename, "r")
    content = file.read()
    datdict[filename] = content
    saveDat()


def readDat():

    if os.path.isfile(root+"/"+"dat.dat"):
        file = open(root+"/"+"dat.dat", "r")
        for line in file:
            if '#' in line:
                (key, val) = line.split('#', 1)
                datdict[key] = val

        file.close()

    else:
        file = open(root+"/"+"dat.dat", "w")

        file.close()


def createFile(filename):
    file = open(filename, "w")
    # filesInUse.append(filename)
    # content = 'text of file 1'
    # file.write(content)
    file.close()
    # filesInUse.remove(filename)
    writeDat(filename)


def deleteFile(filename):
    print(filesInUse)
    if filename not in filesInUse:
        datdict.pop(filename)
        print(filename)
        os.remove(filename)
    else:
        print("File is in use, cannot be deleted!!!")


def makeDirectory(directory):
    if os.path.isdir(directory):
        print("Directory already exists!!!")
    else:
        directoryName = root + "/" + directory
        print(directoryName)
        os.mkdir(directoryName)


def changeDirectory(directory):

    if directory == "..":
        directoryName = root
    else:
        directoryName = root + "/" + directory
        directoryName = directoryName.replace("\n", "")
    print(directoryName)
    if os.path.isdir(directoryName):
        os.chdir(directoryName)
    else:
        print("Directory does not exist!!!")


def moveFile(filename, destination):
    # filename = input("Enter the name of the file you want to move: ")
    
    if os.path.exists(filename):
        if filename in filesInUse:
            print("File is in use, cannot be moved!!!")
        else:
            # directoryName = input(
            #     "Enter the name of the directory you want to move the file to: ")
            directoryName = root + "/" + destination
            if os.path.isdir(directoryName):
                os.rename(filename, directoryName + "/" + filename)
            else:
                print("Directory does not exist!!!")

    else:
        print("File does not exist!!!")


def openFile(filename, mode, content='', startingIndex=0, size=0):
    fileName = filename
    # content = ''.join(content)
    print(filename)
    if os.path.exists(filename):
        if filename in filesInUse:
            print(filesInUse)
            print("File is already open!!!")
        else:
            match mode:
                case 'w':
                    file = open(filename, "r")
                    filesInUse.append(file)
                    contents = file.read()
                    filesInUse.remove(file)
                    file.close()
                    contents = str(contents)
                    # print(contents)
                    # print(startingIndex)
                    if int(startingIndex) > len(contents):
                        startingIndex = len(contents)

                    contents = contents[:int(startingIndex)] + \
                        content + contents[int(startingIndex):]
                    # print(contents)
                    file = open(filename, "w")
                    filesInUse.append(file)
                    # print(content)
                    if (startingIndex == 0):
                        file.write(content)
                    else:
                        file.write(contents)
                    if filename in filesInUse:    
                        filesInUse.remove(filename)
                    file.close()

                case 'a':
                    filename = open(filename, "a")
                    filesInUse.append(filename)
                    content = input("Enter the content to append: ")
                    filename.write(content)

                case 'r':
                    filename = open(filename, "r")
                    filesInUse.append(fileName)
                    print("Contents of " + fileName +
                          ": " + filename.read())
                    filesInUse.remove(fileName)
                    filename.close()
                case 'x':
                    file = open(filename, "r")
                    filesInUse.append(file)
                    index = startingIndex
                    length = size
                    contents = file.read()
                    print(contents[int(index):int(index) + int(length)])
                    file.close()
                case _:
                    print("Invalid mode!!!")

            writeDat(fileName)
    else:
        print("File does not exist!!!")


def moveWithinFile():
    filename = input("Enter the name of the file you want to write to: ")
    if os.path.exists(filename):
        file = open(filename, "r")
        filesInUse.append(file)
        contents = file.read()
        filesInUse.remove(file)
        file.close()
        contents = str(contents)
        moveDataFrom = int(input("Enter starting index: "))
        moveDataTo = int(input("Enter ending index: "))
        lengthOfDataToMove = int(input("Enter length of data to move:"))
        dataToMove = contents[moveDataFrom:moveDataFrom + lengthOfDataToMove]
        contents = contents[:moveDataFrom] + \
            contents[moveDataFrom + lengthOfDataToMove:]
        contents = contents[:moveDataTo] + dataToMove + \
            contents[moveDataTo:]

        file = open(filename, "w")
        filesInUse.append(file)
        file.write(contents)
        filesInUse.remove(file)
        file.close()
        writeDat(filename)

    else:
        print("File does not exist!!!")


def truncateFile(filename, size):
    if os.path.exists(filename):
        fileSize = os.path.getsize(filename)
        if int(size) < fileSize:
            file = open(filename, "r+")
            filesInUse.append(file)
            file.truncate(int(size))
            filesInUse.remove(file)
            file.close()
            writeDat(filename)
        else:
            print("File is already smaller than the size you want to truncate to!!!")
    else:
        print("File does not exist!!!")


def closeFile(filename):
    if filename in filesInUse:
        file = open(filename, "r")
        filesInUse.remove(filename)
        file.close()
    else:
        print("File is not opened")


def memoryMap():
    arr = {}
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            file = open(os.path.join(root, name), "r")
            arr[os.path.join(root, name)] = hex(id(file))

        for name in dirs:
            if os.path.isdir(os.path.join(root, name)) == False:
                file = open(os.path.join(root, name), "r")
                arr[os.path.join(root, name)] = hex(id(file))

        for key, value in arr.items():
            print(key + ':\t' + value+'\n')
        # for name in files:


# functionDic = {
#     'create': createFile(file),
#     'delete': deleteFile(),
#     'mkdir': makeDirectory(),
#     'chDir': changeDirectory(),
#     'move': moveFile(),
#     'open': openFile(),
#     'moveWithin': moveWithinFile(),
#     'truncate': truncateFile(),
#     'close': closeFile(),
#     'memoryMap': memoryMap()
# }

if __name__ == "__main__":
    filenames = ['input.txt', 'input2.txt', 'input3.txt', 'input4.txt']
    # args = sys.argv[1:3]
    nThreads = int(sys.argv[1])
    
    # lines = f.readlines()

    print("Threads: " + str(nThreads))

    for i in range(nThreads):
        f = open(filenames[i], "r")
        lines = f.readlines()

        t = threading.Thread(target=thread_function, args=[i, lines])
        t.start()

# readDat()
# print("Welcome to the file system")
# while True:
#     print('Current working directory: ' + os.getcwd())
#     print('0. Exit')
#     print("1. Create a file")
#     print("2. Delete a file")
#     print("3. Close file")
#     print("4. Create a directory")
#     print("5. Change directory")
#     print("6. Move a file")
#     print("7. Open a file")
#     print("8. Move within a file")
#     print("9. Truncate a file")
#     print("10. Memory map")
#     print("11. List files")

#     mode = input("Enter the mode you want to run the file system in: ")
#     match mode:
#         case '0':
#             print("exiting")
#             break
#         case '1':
#             createFile()
#         case '2':
#             filename = input(
#                 "Enter the name of the file you want to delete: ")
#             deleteFile(filename)
#         case '3':
#             closeFile()
#         case '4':
#             makeDirectory()
#         case '5':
#             changeDirectory()
#         case '6':
#             moveFile()
#         case '7':
#             openFile()
#         case '8':
#             moveWithinFile()
#         case '9':
#             truncateFile()
#         case '10':
#             memoryMap()
#         case '11':
#             showDat()

#         case _:
#             print("Invalid mode!!!")
# saveDat()
# print("Thank you for using the file system")