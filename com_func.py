#! /usr/bin/python
#coding: UTF-8
import argparse

def writeFile(fname, code):
    try:
        with open(fname, 'wb') as f:
		    f.write(''.join(code))
    except IOError:
        exit('No such file or directory ' + fname)


def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            text = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return text		

	
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('outFile')
    return parser.parse_args()	
	

	# Выравнивание потока и добавление длины сообщения
def alignment(msg):
    msg_len = len(msg) * 8
    msg.append(0x80)
    while len(msg)% 64 != 56:
	    msg += [0]  
    for i in range(8):
        msg.append(msg_len >> i * 8)
    return msg	
	
	
def toLittleEndian(word):
    res = 0
    res |= ((word >> 0) & 0xFF) << 24
    res |= ((word >> 8) & 0xFF) << 16
    res |= ((word >> 16) & 0xFF) << 8
    res |= ((word >> 24) & 0xFF) << 0
    return res
	
	
# циклический сдвиг влево на n бит
def rotateLeft(x, n): 
    return ((x << n) | (x >> (32-n))) & 0xFFFFFFFF 	