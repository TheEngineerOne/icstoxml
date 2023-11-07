import re
inFilename = "testsample.ics"
outFilename = "output.xml"
indentationLevel = 0
inFile = open(inFilename,'r',encoding="utf-8")
outFile = open(outFilename,'w',encoding="utf-8")
isOpen = False
outFile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
outFile.write("<array name=\"event_list\">\n")
indentationLevel += 1

def convertDate(date):
    return f"{date[0:4]}-{date[4:6]}-{date[6:8]}T{date[9:11]}:{date[11:13]}:{date[13:15]}"
    

for line in inFile:
    line = line[:-1]
    if(re.search('BEGIN:VEVENT',line)):
        outFile.write("<event>")
        isOpen = True
        indentationLevel += 1
    elif(re.search('END:VEVENT',line)):
            indentationLevel -= 1
            outFile.write("</event>")
            isOpen = False
    elif(isOpen):
        if(re.search("^[^;]*:[^:]*$",line)):
            output = line.split(':')
            if(re.fullmatch("[0-9]{8}T[0-9]{6}Z",output[1])):
                output[1] = convertDate(output[1])
            output[1] = output[1].replace("&","&amp;")
            outFile.write('<' + output[0] + '>')
            outFile.write(output[1])
            outFile.write("</" + output[0] + '>')
            
        elif(re.search("^.*;.*$",line)):
            output = line.split(';')
            outFile.write('<' + output[0] + '>')
            indentationLevel += 1
            output[1] = output[1].split(':',maxsplit=1)
            output[1][1] = output[1][1].split("\\n")
            output[1] = [output[1][0],*output[1][1]]
            for subline in output[1]:
                temp = re.split("[=:]",subline)
                if(re.fullmatch("[0-9]{8}T[0-9]{6}Z",temp[-1])):
                    temp[-1] = convertDate(temp[-1])
                temp[-1] = temp[-1].replace("&","&amp;")
                outFile.write('<' + temp[0].replace(' ', '') + '>')
                outFile.write(temp[-1])
                outFile.write("</" + temp[0].replace(' ', '') + '>')
            indentationLevel -= 1
            outFile.write("</" + output[0] + '>')
outFile.write("</array>")
inFile.close()
outFile.close()