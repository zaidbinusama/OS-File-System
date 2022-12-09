import os

filesInUse = []
root = os.getcwd()
global datdict
datdict = {}


def showDat():
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


def createFile():
    filename = input("Enter a filename: ")
    file = open(filename, "w")
    filesInUse.append(filename)
    content = input("Enter the content of the file: ")
    file.write(content)
    file.close()
    filesInUse.remove(filename)
    writeDat(filename)
    print(filesInUse)


def deleteFile(filename):
    print(filesInUse)
    if filename not in filesInUse:
        datdict.pop(filename)
        print(filename)
        os.remove(filename)
    else:
        print("File is in use, cannot be deleted!!!")


def makeDirectory():
    directoryName = input("Enter the name of the directory: ")
    directoryName = root + "/" + directoryName
    os.mkdir(directoryName)


def changeDirectory():
    directoryName = input(
        "Enter the name of the directory you want to go to: ")
    directoryName = root + "/" + directoryName
    if os.path.isdir(directoryName):
        os.chdir(directoryName)
    else:
        print("Directory does not exist!!!")


def moveFile():
    filename = input("Enter the name of the file you want to move: ")
    if os.path.exists(filename):
        if filename in filesInUse:
            print("File is in use, cannot be moved!!!")
        else:
            directoryName = input(
                "Enter the name of the directory you want to move the file to: ")
            directoryName = root + "/" + directoryName
            if os.path.isdir(directoryName):
                os.rename(filename, directoryName + "/" + filename)
            else:
                print("Directory does not exist!!!")

    else:
        print("File does not exist!!!")


def openFile():
    filename = input("Enter the name of the file you want to open: ")
    fileName = filename
    if os.path.exists(filename):
        if filename in filesInUse:
            print("File is already open!!!")

        else:
            mode = input(
                "Enter the mode you want to open the file in:\n w for write_at\n a for append\n r for read\n x to print section\n")
            match mode:
                case 'w':
                    startingIndex = input("Enter starting index: ")
                    file = open(filename, "r")
                    filesInUse.append(file)
                    userContent = input("Enter the content you want to add: ")
                    contents = file.read()
                    filesInUse.remove(file)
                    file.close()
                    contents = str(contents)

                    if int(startingIndex) > len(contents):
                        startingIndex = len(contents)

                    contents = contents[:int(startingIndex)] + \
                        userContent + contents[int(startingIndex):]
                    file = open(filename, "w")
                    filesInUse.append(file)
                    file.write(contents)

                case 'a':
                    filename = open(filename, "a")
                    filesInUse.append(filename)
                    content = input("Enter the content to append: ")
                    filename.write(content)

                case 'r':
                    filename = open(filename, "r")
                    filesInUse.append(filename)
                    print(filename.read())

                case 'x':
                    file = open(filename, "r")
                    filesInUse.append(file)
                    index = input("Enter starting index: ")
                    length = input("Enter length of data to print: ")
                    contents = file.read()
                    print(contents[int(index):int(index) + int(length)])

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


def truncateFile():
    size = input("Enter new size:")
    filename = input("Enter the name of the file you want to truncate: ")
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


def closeFile():
    filename = input("Enter the name of the file you want to close: ")
    if filename in filesInUse:
        filesInUse.remove(filename)
        filename.close()
    else:
        print("File is not opened")


def memoryMap():
    arr = {}
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            file = open(os.path.join(root, name), "r")
            # print(os.path.join(root, name)+ ':\t' + hex(id(file)))
            arr[os.path.join(root, name)] = hex(id(file))

        for name in dirs:
            if os.path.isdir(os.path.join(root, name)) == False:
                file = open(os.path.join(root, name), "r")
                # print(os.path.join(root, name)+ ':\t' + hex(id(file)))
                arr[os.path.join(root, name)] = hex(id(file))

        for key, value in arr.items():
            print(key + ':\t' + value+'\n')
        # for name in files:


if __name__ == "__main__":
    readDat()
    print("Welcome to the file system")
    while True:
        print('Current working directory: ' + os.getcwd())
        print('0. Exit')
        print("1. Create a file")
        print("2. Delete a file")
        print("3. Close file")
        print("4. Create a directory")
        print("5. Change directory")
        print("6. Move a file")
        print("7. Open a file")
        print("8. Move within a file")
        print("9. Truncate a file")
        print("10. Memory map")
        print("11. List files")

        mode = input("Enter the mode you want to run the file system in: ")
        match mode:
            case '0':
                print("exiting")
                break
            case '1':
                createFile()
            case '2':
                filename = input(
                    "Enter the name of the file you want to delete: ")
                deleteFile(filename)
            case '3':
                closeFile()
            case '4':
                makeDirectory()
            case '5':
                changeDirectory()
            case '6':
                moveFile()
            case '7':
                openFile()
            case '8':
                moveWithinFile()
            case '9':
                truncateFile()
            case '10':
                memoryMap()
            case '11':
                showDat()

            case _:
                print("Invalid mode!!!")
    saveDat()
    print("Thank you for using the file system")
