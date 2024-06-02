"""MCGRandom.py -> Various Hash/random functions
Everything is contained within class MCGRandom (MyComputerGirl's hash/random library)
Main user functions:


CharToInt(InputChar) -> int; Converts indexed chars to int
ConstrainInt(InputVar: int, Min: int, Max: int) -> int; Constraints given ints to given interval
Hash(InputVar: str, Depth = 10) -> int; My own hash function
RandomInt(FunctionSeed = None, Min = 0, Max = 1000000) -> int; Generates random number within given interval
RandomIntWithSetLen(FunctionSeed = None, Length = 25) -> int; Generates random number with set given size
RandomStr(Length = 15, CharList = FullCharList) -> str; Generates random str with given set size
PopCharFromStr(index, string) -> str; Get indexed char from str
ScrambleFullCharList(ThisCharList = FullCharList) -> str; Scrambles given char list for further randomisation
ScrambledRandStr(Length = 64) -> str; Generates random str with randomised char list for maximum scrambling
"""
import math as m
import rpl as rp
import time
from typing import Self

class MCGRandom():
	def __init__(self: Self):
		self.Seed = m.floor(time.time() * 1000)

		self.RPS = rp.RandomisedPrimes
		self.RPL = len(rp.RandomisedPrimes)

		self.CharList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+{}:|<>?"
		self.FullCharList = "FHZdk4a^s=$+~3%bE;pv:[cym9>BoD?K,'!XT0GQ5L(O<1U`N_qC{|Sh#eln}r2J8M*jg). -WfI]6/iz7\\VP@tuYwRA&x"
		self.AlphaNumericList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		self.RussianList = "йцукенгшщзхъфывапролджэячсмитьбю"

		self.AbsoluteFull = self.FullCharList + self.RussianList

		self.SortedFullCharList = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[];'\\,./{}:||<>? "

	def CharToInt(self: Self, InputChar: str) -> int:
		return self.SortedFullCharList.find(InputChar)

	#Function to constrain InputVar to be within range of Min to Max
	def ConstrainInt(self: Self, InputVar: int, Min: int, Max: int) -> int:
		return (InputVar % (Max - Min)) + Min 

	#My own cryptographic Hash function
	def Hash(self: Self, InputVar: str, Depth = 10) -> int:
		InputVar = str(InputVar)
		
		#Initiate list q
		q = [0 for i in range(Depth)]
		for i, char in enumerate(InputVar):
			q[0] *= len(self.SortedFullCharList)
			q[0] += self.CharToInt(char)
		
		#Compute Hash function with depth Depth
		for i in range(1, Depth):
			t = q[i-1]	#Short-hand name for previous value

			PartOne = t + self.RPS[t % self.RPL] + self.RPS[(self.RPS[t % self.RPL] + 5) % self.RPL] + self.RPS[(self.RPL - (t + 11)) % self.RPL]
			PartOneInsidePartTwo = t + self.RPS[(t + 19) % self.RPL]
			PartTwoInsidePartTwo = self.RPS[(self.RPL - (t % self.RPL) + 7) % self.RPL] + 23
			PartThreeInsidePartTwo = self.RPL
			PartTwo = self.RPS[(PartOneInsidePartTwo + PartTwoInsidePartTwo) % PartThreeInsidePartTwo]

			q[i] = PartOne % PartTwo
		
		#Negative outputs are possible, so to normalize for positive numbers only
		if q[Depth-1] < 0:
			q[Depth-1] *= -1
		
		return q[Depth-1]

	#My own random number generator with minimum and maximum values for output
	def RandomInt(self: Self, FunctionSeed = None, Min = 0, Max = 1000000) -> int:
		if FunctionSeed is None:
			FunctionSeed = self.Seed
		
		q = self.Hash(str(FunctionSeed + m.floor(time.time() * 1000))) * self.Hash(str(FunctionSeed + m.floor(time.time() * 11))) + self.Hash(str(FunctionSeed + m.floor(time.time())))
		self.Seed = q

		DividingSize = 10**30
		if Min > DividingSize:
			while Min > DividingSize:
				q *= self.RandomInt(self.Seed, DividingSize, Max)
				Min /= DividingSize
		
		return self.ConstrainInt(q, Min, Max)

	#my own Hash function with set length int output
	def RandomIntWithSetLen(self: Self, FunctionSeed = None, Length = 25) -> int:
		q = 0
		
		if FunctionSeed is None:
			FunctionSeed = self.Seed
		
		#Calculate length needed for appropriate output
		if Length - 17 <= 1:
			leng = 1
		else:
			leng = Length - 17
		
		#Compute Hash function
		for i in range(leng):
			q += self.Hash(str(FunctionSeed + m.floor(time.time() * 1000))) * self.Hash(str(FunctionSeed + m.floor(time.time() * 11))) + self.Hash(str(FunctionSeed + m.floor(time.time())))
		
		#Ensure propper output length
		qq = ""
		for i in range(Length):
			qq += str(q[i])
		
		return int(qq)

	#My own random string generator with defined length for output
	def RandomStr(self: Self, Length: int, CharList: str | None = None) -> str:
		q = ""

		if CharList is None:
			CharList = self.FullCharList
		
		#Compute Hash function based on character set CharList
		for i in range(Length):
			q += CharList[self.RandomInt(None,0,len(CharList)-1)]
		
		return q

	#Pop a singular character from a string
	def PopCharFromStr(self: Self, index: int, string: str) -> str:
		if index == 0:
			return string[1:]
		
		return string[0] + self.PopCharFromStr(index-1, string[1:])

	#Scramble the whole character set string
	def ScrambleFullCharList(self: Self, ThisCharList: str | None = None) -> str:
		q = ""

		if ThisCharList is None:
			ThisCharList = self.FullCharList

		for i in range(len(ThisCharList)):
			t = self.RandomInt(None, 0, len(ThisCharList))
			q += ThisCharList[t]
			ThisCharList = self.PopCharFromStr(t, ThisCharList)
		
		return q

	#Random string using scrambling
	def ScrambledRandStr(self: Self, Length = 64) -> str:
		q = ""
		CharList = ""
		for i in range(self.RandomInt(None, 1, 3)):
			CharList += self.ScrambleFullCharList()
		
		#Compute Hash function based on character set CharList while scrambling it
		for i in range(Length):
			q += CharList[self.RandomInt(None,0,len(CharList)-1)]
			CharList = self.ScrambleFullCharList(CharList)
		
		return q
