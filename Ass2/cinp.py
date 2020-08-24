import pydiff
import ctypes

seq1 = b'AGTC'
seq2 = b'AGTC'

bbq = pydiff.py_get_distance(b'A',b'T')
print('Distance is', bbq)

ppg = pydiff.py_get_min(3,4)
print('Min is', ppg)


fun = ctypes.cdll.LoadLibrary(r"G:\Study\2-2\DataMining\Ass2\libdiff.so")
returnValue = fun.get_distance(seq1, seq2)
print('Got distance', returnValue)
