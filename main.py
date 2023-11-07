import re
inFilename = "testsample.ics"
outFilename = "output.xml"
indentationLevel = 0
inFile = open(inFilename,'r',encoding="utf-8")
outFile = open(outFilename,'w',encoding="utf-8")
isOpen = False

for line in inFile:
    line = line[:-1]
    if(re.search('BEGIN:VEVENT',line)):
        outFile.write("<event>" +'\n')
        isOpen = True
        indentationLevel += 1
    elif(re.search('END:VEVENT',line)):
            outFile.write("</event>" + '\n')
            isOpen = False
            indentationLevel -= 1
    elif(isOpen):
        if(re.search('^[^;]*:[^:]*$',line)):
            output = line.split(':')
            outFile.write(indentationLevel*"\t" + '<' + output[0] + '>' + '\n')
            outFile.write((indentationLevel+1)*"\t" +output[1]+ '\n')
            outFile.write(indentationLevel*"\t" + "</" + output[0] + '>' +'\n')
        elif(re.search("^.*;.*$",line)):
            output = line.split(';')
            outFile.write(indentationLevel*"\t" + '<' + output[0] + '>' + '\n')
            indentationLevel += 1
            output[1] = output[1].split(':',maxsplit=1)
            output[1][1] = output[1][1].split("\\n")
            output[1] = [output[1][0],*output[1][1]]
            for subline in output[1]:
                temp = re.split("[=:]",subline)
                outFile.write(indentationLevel*"\t" + '<' + temp[0] + '>' + '\n')
                outFile.write((indentationLevel+1)*"\t" + temp[-1] + '\n')
                outFile.write(indentationLevel*"\t" + "</" + temp[0] + '>' + '\n')
            indentationLevel -= 1
            outFile.write(indentationLevel*"\t" + "</" + output[0] + '>' + '\n')
inFile.close()
outFile.close()