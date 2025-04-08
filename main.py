import curses
import time
import random
from curses import wrapper

def startScreen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Typing Speed Test")
    stdscr.addstr("\nPress any key to begin the test!")
    stdscr.refresh()
    stdscr.getkey()
    
def displayText(stdscr, targetText, currentText, counter = 0):
        stdscr.addstr(targetText)
        stdscr.addstr(3, 0, "Words per minute: " + str(counter))
        
        for i, c in enumerate(currentText):
            correctChar = targetText[i]
            color = curses.color_pair(1)
            
            if c != correctChar:
                color = curses.color_pair(2)
            
            stdscr.addstr(0, i, c, color)
    
def generatePhrase():
    with open("phrases.txt", "r") as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def typeSpeed(stdscr):
    text = generatePhrase()
    currentText = []
    counter = 0
    startingTime = time.time()
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startingTime, 1)
        counter = round((len(currentText) / (timeElapsed / 60)) / 5)
        
        if "".join(currentText) == text:
            stdscr.nodelay(False)
            break
        
        stdscr.clear()    
        displayText(stdscr, text, currentText, counter)
        stdscr.refresh()
        
        try:
            key = stdscr.getkey()
        except:
            continue
        
        if ord(key) == 27: #ASCII Code for the escape button
            break
        
        if key in ("KEY_BACKSPACE", '\b', "\x7f"): #Check if the clicked key is a backspace
            if (len(currentText) > 0) :
                currentText.pop() #Remove the previously typed letter
        elif len(currentText) < len(text):
            currentText.append(key)



def main(stdscr):
    
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    startScreen(stdscr)
    
    while True:
        typeSpeed(stdscr)
        
        stdscr.addstr(4, 0, "You have completed the text! Press any key to continue...")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break

wrapper(main)
