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

    _download_location_ = "https://dl.dropbox.com/u/2862706/ice_emulators/Winbsnes.zip"
    _relative_exe_path_ = os.path.join("Winbsnes","bsnes.exe")

    __invalid_extensions__ = [
        ".sav", # NES and Gameboy save file
        ".srm"  # SNES save file
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
        
    def set_control_scheme(self,controls):
        """
        bsnes keeps it's control scheme in a flat file called input.cfg.
        """
        control_map = self.control_map(controls)
        def replacement_function(line):
            # Our line identifies a control which we want to change
            if line.startswith(self.control_prefix()):
                identifier = line[:line.index(' ')]
                try:
                    control = control_map[identifier]
                    control_value = controls[control]
                    if control_value != "":
                        return "%s = \"%s\"\n" % (identifier,control_value)
                # We have an identifier which starts with the prefix, but isn't
                # managed by Ice. Use the current value
                except KeyError:
                    return line
            return line
        self.replace_contents_of_file(self.path_for_input_file(),replacement_function)
   
    def path_for_input_file(self):
        """
        Returns the path to the downloaded emulators input.cfg
        """
        return os.path.join(self.directory,"input.cfg")
        
    def identifier_for_control(self,button):
        return "%s%s" % (self.control_prefix(),button)
        
    def control_prefix(self):
        """
        Returns the prefix used by input.cfg to represent the controller. The
        result of the function should be a prefix which, when appended with the
        button name (A,B,X,Y,etc) should generate a valid identifier in 
        input.cfg
        
        Ex...
        
        NES => "Famicom::ControllerPort1::Gamepad::"
        
        This is valid because the identifier for the Up button is
        
        Famicom::ControllerPort1::Gamepad::Up
        """
        return {
            "NES":      "Famicom::ControllerPort1::Gamepad::",
            "SNES":     "SuperFamicom::ControllerPort1::Gamepad::",
            "Gameboy":  "GameBoy::Device::Controller::",
            "GBA":      "GameBoyAdvance::Device::Controller::"
        }[self._console_name_]
        
    def control_map(self,controls):
        cmap = {}
        for control in controls.keys():
            capitalized = control.title() # Capitializes the control name
            iden = self.identifier_for_control(capitalized)
            cmap[iden] = control
        return cmap