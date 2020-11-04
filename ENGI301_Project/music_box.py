"""
--------------------------------------------------------------------------
Combination Lock
--------------------------------------------------------------------------
License:   
Copyright 2020 Michael Tang

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""
from sound import *
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import threading

import ht16k33 as HT16K33

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


class MusicBox():
    # note buffers for each speaker
    buffer_0 = []
    buffer_1 = []
    buffer_2 = []
    
    # pins corresponding to each speaker
    speaker_0 = None
    speaker_1 = None
    speaker_2 = None
    
    # dict to store pins corresponding to each note
    note_pins = {}
    
    # pin corresponding to switch
    switch = None
    
    # object representing 7-segment display
    
    # list of possible notes
    notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    def __init__(self, speaker_0="P1_36", speaker_1="P1_33", speaker_2="P2_1", C="P1_17", D="P1_19", E="P1_21", F="P1_23", G="P1_25", A="P1_27", B="P2_36", switch="P2_2", i2c_bus=1, i2c_address=0x70):
        # initialize speaker pins
        self.speaker_0 = speaker_0
        self.speaker_1 = speaker_1
        self.speaker_2 = speaker_2

        # initialize note pins
        self.C = C
        self.D = D
        self.E = E
        self.F = F
        self.G = G
        self.A = A
        self.B = B
        
        # initialize switch pin
        self.switch = switch
        
        # initialize 7-segment display
        self.display = HT16K33.HT16K33(i2c_bus, i2c_address)
        
        self._setup()
    
    def _setup(self):
        # Initialize Display
        self.set_display_off()
        
        # Initialize Switch
        GPIO.setup(self.switch, GPIO.IN)
        
        # Initialize Analog Inputs
        ADC.setup()
            
    
    def run(self):
        # only start running music box if switch is on
        while(self.check_switch()):
            pass
            # turn on motor
            
            # check each input pin to see if certain notes are being played
        

    def check_switch(self):
        """
        Checks if switch is on or off
        
        Input: None
        Output: True if switch is on, false otherwise
        """
        return (GPIO.input(self.switch) == 1)
        
        
    def set_display_off(self):
        """
        Set display to "off"
        """
        self.display.set_digit_raw(0, 0x3F)        # "O"
        self.display.set_digit_raw(1, 0x71)        # "F"
        self.display.set_digit_raw(2, 0x71)        # "F"
        self.display.set_digit_raw(3, 0x00)        # " "
        
if __name__ == '__main__':
    test = MusicBox()