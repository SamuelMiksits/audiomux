import os
import re
import subprocess

#returns a list of the sinks
def getSinks():
    sinksRaw = re.split(r"[\t\n]", subprocess.getoutput("pactl list sinks"))
    return parseSinks(sinksRaw)

#returns a list of the sources
def getSources():
    sourcesRaw = re.split(r"[\t\n]", subprocess.getoutput("pactl list sources"))
    return parseSources(sourcesRaw)

#grabs the default sink
def getDefaultSink():
    return subprocess.getoutput("pactl get-default-sink")

#grabs the default source
def getDefaultSource():
    return subprocess.getoutput("pactl get-default-source")

#parses sinks string returned from shell
def parseSinks(sinksRaw):
    sinks = list()
    tmpSink = list()
    for sink in sinksRaw:
        if "Name" in sink:
            tmpSink.append(sink.lstrip("Name:"))
        if "Description" in sink:
            tmpSink.append(sink.lstrip("Description: "))
            sinks.append(tmpSink)
            tmpSink = list()
    return sinks

#parses sources string returned from shell
def parseSources(sourcesRaw):
    sources = list()
    tmpSource = list()
    for source in sourcesRaw:
        if "Name" in source:
            tmpSource.append(source.lstrip("Name:"))
        if "Description" in source:
            tmpSource.append(source.lstrip("Description: "))
            sources.append(tmpSource)
            tmpSource = list()
    return sources

def main():

    exitProgram = False 

    while(not exitProgram):
        
        os.system("clear")
        sinks = getSinks()
        sources = getSources()
        fullList = sinks.copy()
        for i in range(len(sources)):
            fullList.append(sources[i])

        defaultSink = getDefaultSink()
        defaultSource = getDefaultSource()

        defaultSinkAt = 0 #find where it is in the sinks list, grab description
        defaultSourceAt = 0

        for i in range(len(sinks)):
            if defaultSink in sinks[i][0]:
                defaultSinkAt = i
        
        for i in range(len(sources)):
            if defaultSource in sources[i][0]:
                defaultSourceAt = i

        print("Active sink/source:")

        print("Default sink: ", end="")
        print(sinks[defaultSinkAt][1])

        print("Default source: ", end="")
        print(sources[defaultSourceAt][1])

        print("------------------------------")

        print("Selectable sinks/sources:")

        j = 0
        print("Sinks: ")
        for i in range(len(sinks)):
            print(str(j + 1) + ". ", end="")
            print(sinks[i][1])
            j += 1

        print("Sources: ")
        for i in range(len(sources)):
            print(str(j + 1) + ". ", end="")
            print(sources[i][1])
            j += 1

        print("Select sink/source with number, 'e' for exit, any input to refresh list")
        userInput = input()

        userInputParsed = -1

        try:
            userInputParsed = int(userInput) - 1
        except:
            try:
                if userInput == "e":
                    exitProgram = True
                    continue              
            except:
                pass
        
        if (userInputParsed >= 0) and (userInputParsed < len(fullList)):
            if userInputParsed < len(sinks):
                os.system("pactl set-default-sink " + sinks[userInputParsed][0]) 

            if userInputParsed >= len(sinks):
                os.system("pactl set-default-source " + sources[userInputParsed - len(sinks)][0]) 

if __name__ == "__main__":
    main()