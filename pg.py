"""pg.py -> Various Hash functions
Main user functions:


constrain(InputVar: int, Min: int, Max: int) -> Constraints InputVar to within given range
CoreHash(InputVar: str, Depth = 10) -> My Own Proprietary Hash function
Hash(InputVar: int, Depth = 10, StringLength = 10) -> Expanded Hash function to handle arbitrary length inputs
rand(FunctionSeed = None, Min = 0, Max = 1000000) -> Random number generator with automatic seed update
RandLen(FunctionSeed = None, Length = 25) -> Set length output random number generator
RandStr(Length = 15, CharList = CharList) -> Random string generator using CharList as character set and set length
"""
import math as m
import rshps as rp
import time

RPS = rp.rshps
RPL = len(rp.rshps)

Seed = m.floor(time.time() * 1000)

CharList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}:|<>?"
FullCharList = "FHZdk4a^s=$+~3%bE;pv:[cym9>BoD?K,'!XT0GQ5L(O<1U`N_qC{|Sh#eln}r2J8M*jg). -WfI]6/iz7\VP@tuYwRA&x"
AlphaNumericList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

SortedFullCharList = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[];'\\,./{}:||<>? "

def CharToInt(InputChar):
	return SortedFullCharList.find(InputChar)

#Function to constrain InputVar to be within range of Min to Max
def constrain(InputVar: int, Min: int, Max: int):
	return (InputVar % (Max - Min)) + Min 

#My own cryptographic Hash function
def Hash(InputVar: str, Depth = 10):
	InputVar = str(InputVar)
	
	#Initiate list q
	q = [0 for i in range(Depth)]
	for i, char in enumerate(InputVar):
		q[0] *= len(SortedFullCharList)
		q[0] += CharToInt(char)
	
	#Compute Hash function with depth Depth
	for i in range(1, Depth):
		t = q[i-1]	#Short-hand name for previous value
		q[i] = (t + RPS[t % RPL] + RPS[(RPS[t % RPL] + 5) % RPL] + RPS[(RPL - (t + 11)) % RPL]) % RPS[(t + RPS[(t + 19) % RPL] + RPS[(RPL - (t % RPL) + 7) % RPL] + 23) % RPL]
	
	#Negative outputs are possible, so to normalize for positive numbers only
	if q[Depth-1] < 0:
		q[Depth-1] *= -1
	
	return q[Depth-1]

#My own random number generator with minimum and maximum values for output
def rand(FunctionSeed = None, Min = 0, Max = 1000000):
	global Seed
	
	#Initiate FunctionSeed if not defined
	if FunctionSeed == None:
		FunctionSeed = Seed
	
	#Set new Seed
	q = Seed = Hash(str(FunctionSeed + m.floor(time.time() * 1000))) * Hash(str(FunctionSeed + m.floor(time.time() * 11))) + Hash(str(FunctionSeed + m.floor(time.time())))
	
	return constrain(q, Min, Max)

#my own Hash function with set length int output
def RandLen(FunctionSeed = None, Length = 25):
	global Seed
	
	#Initiate FunctionSeed if not defined
	if FunctionSeed == None:
		FunctionSeed = Seed
	
	q = ""
	
	#Calculate length needed for appropriate output
	if Length - 17 <= 1:
		leng = 1
	else:
		leng = Length - 17
	
	#Compute Hash function
	for i in range(leng):
		q += str(Hash(str(FunctionSeed + m.floor(time.time() * 1000))) * Hash(str(FunctionSeed + m.floor(time.time() * 11))) + Hash(str(FunctionSeed + m.floor(time.time()))))
	
	#Ensure propper output length
	qq = ""
	for i in range(Length):
		qq += str(q[i])
	
	return qq

#My own random string generator with defined length for output
def RandStr(Length = 15, CharList = FullCharList):
	q = ""
	
	#Compute Hash function based on character set CharList
	for i in range(Length):
		q += CharList[rand(None,0,len(CharList)-1)]
	
	return q

#Pop a singular character from a string
def PopCharFromStr(index, string):
	if index == 0:
		return string[1:]
	return string[0] + PopCharFromStr(index-1, string[1:])

#Scramble the whole character set string
def ScrambleFullCharList(FullCharList = FullCharList):
	q = ""
	for i in range(len(FullCharList)-1):
		t = rand(None, 1, len(FullCharList))
		q += FullCharList[t]
		FullCharList = PopCharFromStr(t, FullCharList)
	return q

#Random string using scrambling
def ScrambledRandStr(Length = 64):
	q = ""
	CharList = ""
	for i in range(rand(None, 1, 3)):
		CharList += ScrambleFullCharList()
	
	#Compute Hash function based on character set CharList while scrambling it
	for i in range(Length):
		q += CharList[rand(None,0,len(CharList)-1)]
		CharList = ScrambleFullCharList(CharList)
	
	return q

def HashFile(path, Depth=10):
	fh = open(path, "r")
	lines = fh.readlines()
	Hashed_lines = []
	for i, e in enumerate(lines):
		char_code_line = ""
		for ii, ee in enumerate(e):
			char_code_line += str(ord(ee))
		t = str(i) + char_code_line
		Hashed_lines.append(Hash(t, Depth))
	master_Hash = ""
	for e in Hashed_lines:
		master_Hash += str(e)
	return Hashed_lines, Hash(master_Hash)

