
import math as m
import rshps as rp
import time

RPS = rp.rshps
RPL = len(rp.rshps)

Seed = m.floor(time.time() * 1000)

CharList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}:|<>?"
AlphaNumericList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#Function to constrain InputVar to be within range of Min to Max
def constrain(InputVar: int, Min: int, Max: int):
	return (InputVar % (Max - Min)) + Min 

#My own cryptographic hash function
def CoreHash(InputVar: str, Depth = 10):
	InputVar = str(InputVar)
	
	#Initiate list q
	q = [0 for i in range(Depth)]
	q[0] = int(InputVar,36)
	
	#Compute hash function with depth Depth
	for i in range(1, Depth):
		t = q[i-1]	#Short-hand name for previous value
		q[i] = (t + RPS[t % RPL] + RPS[(RPS[t % RPL] + 5) % RPL] + RPS[(RPL - (t + 11)) % RPL]) % RPS[(t + RPS[(t + 19) % RPL] + RPS[(RPL - (t % RPL) + 7) % RPL] + 23) % RPL]
	
	#Negative outputs are possible, so to normalize for positive numbers only
	if q[Depth-1] < 0:
		q[Depth-1] *= -1
	
	return q[Depth-1]

#Function to handle larger input sized without problems of converting to int
def hash(InputVar: int, Depth = 10, StringLength = 10):
	inputs = []
	t = ""
	
	#Partition InputVar to appropriate sizes
	for i, e in enumerate(InputVar):
	
		#If the length of the string is one less than the length desired, append to inputs and reset t
		if i % StringLength == StringLength - 1:
			inputs.append(t)
			t = ""
		
		t += e
	
	#Compute final output
	qs = 0
	for i, e in enumerate(inputs):
		qs += CoreHash(e, Depth)
	
	return qs % CoreHash(qs,Depth)


#My own random number generator with minimum and maximum values for output
def rand(FunctionSeed = None, Min = 0, Max = 1000000):
	global Seed
	
	#Initiate FunctionSeed if not defined
	if FunctionSeed == None:
		FunctionSeed = Seed
	
	#Set new Seed
	q = Seed = hash(str(FunctionSeed + m.floor(time.time() * 1000))) * hash(str(FunctionSeed + m.floor(time.time() * 11))) + hash(str(FunctionSeed + m.floor(time.time())))
	
	return constrain(q, Min, Max)

#my own hash function with set length int output
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
	
	#Compute hash function
	for i in range(leng):
		q += str(hash(str(FunctionSeed + m.floor(time.time() * 1000))) * hash(str(FunctionSeed + m.floor(time.time() * 11))) + hash(str(FunctionSeed + m.floor(time.time()))))
	
	#Ensure propper output length
	qq = ""
	for i in range(Length):
		qq += str(q[i])
	
	return qq

#My own random string generator with defined length for output
def RandStr(Length = 15, CharList = CharList):
	q = ""
	
	#Compute hash function based on character set CharList
	for i in range(Length):
		q += CharList[rand(None,0,len(CharList)-1)]
	
	return q
