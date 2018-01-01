#https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
import ctypes
from time import sleep

keyDictionary = {"'":0x28, "-":0x0c, ",":0x33, ".":0x34, "/":0x35, "[":0x1A, "\\":0x2B, "]":0x1B, "`":0x29, "=":0x0D, "0":0x0B, "1":0x02, "2":0x03,"3":0x04,"4":0x05,"5":0x06,"6":0x07,"7":0x08,"8":0x09,"9":0x0A,"A":0x1E,"ALT":0x38,"B":0x30,"BACKSPACE":0x0E,"C":0x2E,"CAPSLOCK":0x3A,"CTRL":0x1D,"D":0x20,"DEL":0xD3,"DOWNARROW":0xD0,"E":0x12,"END":0xCF,"ENTER":0x1C,"ESCAPE":0x01,"F":0x21,"F1":0x3B,"F10":0x44,"F11":0x57,"F12":0x58,"F2":0x3C,"F3":0x3D,"F4":0x3E,"F5":0x3F,"F6":0x40,"F7":0x41,"F8":0x42,"F9":0x43,"G":0x22,"H":0x23,"HOME":0xC7,"I":0x17,"INS":0xD2,"J":0x24,"K":0x25,"KP_5":0x4C,"KP_DEL":0x53,"KP_DOWNARROW":0x50,"KP_END":0x4F,"KP_ENTER":0x9C,"KP_HOME":0x47,"KP_INS":0x52,"KP_LEFTARROW":0x4B,"KP_MINUS":0x4A,"KP_MULTIPLY":0x37,"KP_PGDN":0x51,"KP_PGUP":0x49,"KP_PLUS":0x4E,"KP_RIGHTARROW":0x4D,"KP_SLASH":0xB5,"KP_UPARROW":0x48,"L":0x26,"LEFTARROW":0xCB,"LWIN":0xDB,"M":0x32,"N":0x31,"NUMLOCK":0x45,"O":0x18,"P":0x19,"PGDN":0xD1,"PGUP":0xC9,"Q":0x10,"R":0x13,"RCTRL":0x9D,"RIGHTARROW":0xCD,"RSHIFT":0x36,"RWIN":0xDC,"S":0x1F,"SCROLLOCK":0x46,"SEMICOLON":0x27,"SHIFT":0x2A,"SPACE":0x39,"T":0x14,"TAB":0x0F,"U":0x16,"UPARROW":0xC8,"V":0x2F,"W":0x11,"X":0x2D,"Y":0x15,"Z":0x2C}

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press(key,t=0.5):
    hexK = keyDictionary[key]
    PressKey(hexK)
    sleep(t)
    ReleaseKey(hexK)
    sleep(t)

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
#while (True):
#    x = raw_input()
#    PressKey(x)
#    sleep(0.5)
#    ReleaseKey(x)
#    sleep(0.5)
