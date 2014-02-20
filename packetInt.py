#!/usr/bin/env python
# encoding: utf-8


def packetInt(intValue,size) :
    #255 的个数
    num255 = size-1
    #余数
    remaiderNum = intValue % 255
    s = chr(255)*num255 + chr(remaiderNum)
    return s

s = packetInt(257,2)
print s

print chr(97)*3
b=257 % 255
print b
