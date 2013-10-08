#!/usr/bin/env python
# encoding: utf-8
"""
winbsnes.py

Created by Scott on 2013-01-07.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

import downloaded_emulator

class Winbsnes(downloaded_emulator.DownloadedEmulator):

    __invalid_extensions__ = [
        ".sav", # NES and Gameboy save file
        ".srm", # SNES save file
        ".bst", # bsnes Save State
    ]

    def __init__(self,console_name):
        super(Winbsnes,self).__init__(console_name)

    def valid_rom(self,path):
        """
        bsnes does an annoying thing where it stores all of the relavant ROM
        information in the same directory as the ROM, which means that our
        beautiful ROM directory gets filled with stuff likes saves. I have
        tried to find a setting to stop that, but can't seem to make it work.
        Instead, I will make sure that the bsnes object doesn't allow Ice to
        add any files that were auto generated by bsnes.
        """
        romname, romext = os.path.splitext(path)
        if romext in self.__invalid_extensions__:
            return False
        return True
        
    def command_string(self,rom):
        """
        Bsnes uses the standard windows command string:
        
        "C:\Path\\to\\bsnes" "C:\Path\\to\ROM"
        """
        return "\"%s\" \"%s\"" % (self.location,rom.path)