import os
import re
import subprocess
import curses

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

def isDefault(default):
    if default:
        return "X"
    else:
        return ""

#Function for printing sink/source
def printSinkSource(menu, strings, index, default):

    if len(strings) == 1:
        menu.addstr("  {:<3} {:<60}   {:<10}\n".format(str(index + 1) + ".", 
                    strings[0], isDefault(default)))

    else:
        menu.addstr("  {:<3} {:<60}   {:<10}\n".format(str(index + 1) + ".", 
                    strings[0], isDefault(default)))
        for i in range(1, len(strings)):
            menu.addstr("{:<6}{:<60}   {:<10}\n".format("", strings[i], ""))
            

# Function that prints the curses menu, takes the menu object
def drawMenu(menu, sinks, sources, index, sinkCount, sourceCount, 
             defaultSink, defaultSource):
    
    #Clears the screen from previous iterations
    menu.clear()

    #Print title
    menu.move(1,2)
    menu.addstr("{:^78}".format("Audiomux - v0.2.0"))
    

    #Print "sinks" header
    menu.move(3, 0)
    menu.addstr("  {:<65}  {:<7}".format("Sink/Output:", "Active"))
    menu.hline(4, 0, 0, 79)
    menu.move(5, 0)

    #Print sinks
    for i in range(len(sinks)):
        if i == index:
            menu.attron(curses.A_REVERSE)
            if i == defaultSink:
                printSinkSource(menu, sinks[i][1], i, True)
            else:
                printSinkSource(menu, sinks[i][1], i, False)
            menu.attroff(curses.A_REVERSE)
        else:
            if i == defaultSink:
                printSinkSource(menu, sinks[i][1], i, True)
            else:
                printSinkSource(menu, sinks[i][1], i, False)


    #Print "sources" header
    menu.hline(5 + sinkCount, 0, 0, 79)
    menu.move(6 + sinkCount, 0)
    menu.addstr("  {:<65}  {:<7}".format("Source/Input:", "Active"))
    menu.hline(7 + sinkCount, 0, 0, 79)
    menu.move(8 + sinkCount, 0)

    #Print sources
    #Print sinks
    for i in range(len(sources)):
        if i + len(sinks) == index:
            menu.attron(curses.A_REVERSE)
            if i == defaultSource:
                printSinkSource(menu, sources[i][1], i + len(sinks), True)
            else:
                printSinkSource(menu, sources[i][1], i + len(sinks), False)
            menu.attroff(curses.A_REVERSE)
        else:
            if i == defaultSource:
                printSinkSource(menu, sources[i][1], i + len(sinks), True)
            else:
                printSinkSource(menu, sources[i][1], i + len(sinks), False)

    #Print "hotkeys"
    menu.hline(8 + sinkCount + sourceCount, 0, 0, 79)
    menu.move(9 + sinkCount + sourceCount, 2)
    menu.addstr("  Set active: s    Down: ")
    menu.addch(curses.ACS_DARROW)
    menu.addstr("/j    Up: ")
    menu.addch(curses.ACS_UARROW)
    menu.addstr("/k    Quit: e/q/<RET>    Refresh: Any")

    #Print box
    menu.box(0,0)
    menu.refresh()

def main():

    stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    #Disable cursor
    curses.curs_set(0)

    numbers = [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'),
               ord('6'), ord('7'), ord('8'), ord('9')]

    ch = 0
    index = 0

    menu = None

    #width:
    # -Original implementation, set to 80
    # -(Potential future feature, calculate maximum allowed rows, adjust text 
    # accordingly)
    width = 80

    # newwin:
    # height, width, offsety, offsetx
    # set offset height/width to make it not snug up against the edge of the 
    # terminal 
    while True:

        sinks = getSinks()
        sources = getSources()

        defaultSink = getDefaultSink()
        defaultSource = getDefaultSource()

        defaultSinkAt = 0
        defaultSourceAt = 0

        #Find default sink
        for i in range(len(sinks)):
            if defaultSink in sinks[i][0]:
                defaultSinkAt = i
            
        #Find default source
        for i in range(len(sources)):
            if defaultSource in sources[i][0]:
                defaultSourceAt = i

        #Convert sink description string into chunks of 60 characters
        for i in range(len(sinks)):
            
            stringRaw = sinks[i][1]
            tmpList = list()
            while len(stringRaw) > 60:
                tmpList.append(stringRaw[0:60])
                stringRaw = stringRaw[60:]

            tmpList.append(stringRaw)
            sinks[i][1] = tmpList


        #Convert source description string into chunks of 60 characters
        for i in range(len(sources)):
            
            stringRaw = sources[i][1]
            tmpList = list()
            while len(stringRaw) > 60:
                tmpList.append(stringRaw[0:60])
                stringRaw = stringRaw[60:]

            tmpList.append(stringRaw)
            sources[i][1] = tmpList

        #Size of the window:
        #height:
        # -1 row of border
        # -1 row for title
        # -1 row for border
        # -1 row for the "sinks" header
        # -1 row for another border
        # -The amount of sinks
        # -1 row for another border
        # -1 row for the "sources" border
        # -1 row for another border
        # -The amount of sources
        # -1 row for another border
        # -1 row for the hotkeys
        # -1 row of empty space
        # -1 row for navigator (type number and jump to that item)
        # -1 row for the bottom border

        sinkCount = 0
        for i in range(len(sinks)):
            sinkCount += len(sinks[i][1])
        sourceCount = 0
        for i in range(len(sources)):
            sourceCount += len(sources[i][1])

        height = 5 + sinkCount + 3 + sourceCount + 5

        #Clears menu, needed in case old menu had different size than new menu
        if menu != None:
            menu.clear()
            menu.refresh()

        #Create menu

        menu = curses.newwin(height, width, 0, 0)
        menu.keypad(True)
        menu.box
    
        drawMenu(menu, sinks, sources, index, sinkCount, sourceCount,
                    defaultSinkAt, defaultSourceAt)
        
        try:
            ch = menu.getch()
        except KeyboardInterrupt:
            break

        if (ch == curses.KEY_DOWN or ch == ord('j')) and \
            (index < (len(sinks) + len(sources) - 1)):
            index += 1

        if (ch == curses.KEY_UP or ch == ord('k')) and \
            (index > 0):
            index -= 1

        if (ch in numbers):
            menu.move(5 + sinkCount + 3 + sourceCount + 5 - 2 , 2)
            menu.addstr(str(ch - 48))
            menu.refresh()
            
            ch2 = menu.getch()

            if ch2 in numbers or ch2 == 48:
                index = (ch - 48)*10 + (ch2 - 48) - 1

            elif ch2 == 10:
                index = (ch - 48) - 1

            elif ch2 == ord("j"):
                index += (ch - 48)

            elif ch2 == ord("k"):
                index -= (ch - 48)

            if index >= len(sources) + len(sinks):
                index = len(sources) + len(sinks) - 1

            if index <= 0:
                index = 0
         
        # 10 = <RET> 
        if ch == ord('q') or ch == ord('e') or ch == 10:
            break 

        if ch == ord('s'):
            if index < len(sinks):
                defaultSinkAt = index
                os.system("pactl set-default-sink " + sinks[defaultSinkAt][0])
            else:
                defaultSourceAt = index - len(sinks)
                os.system("pactl set-default-source " + \
                          sources[defaultSourceAt][0])
                
        stdscr.clear()

    curses.endwin()

if __name__ == "__main__":
    main()