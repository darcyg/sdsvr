#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


gTextCoding = "utf-8"


# pythonString can be a UTF-8 string
def DBM_utlToString(pythonString):
    global gTextCoding
    return bytes(pythonString.encode(gTextCoding))
