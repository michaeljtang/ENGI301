"""
--------------------------------------------------------------------------
Music Box
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
from motor import *
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import threading

import ht16k33 as HT16K33

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
THRESHOLD = 50

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
music_box_on = False

class MusicBox():
    # pins corresponding to each speaker, and a dictionary for storing each speaker's threads
    speaker_0 = None
    speaker_1 = None
    speaker_2 = None
    speaker_threads = []
    
    # dict to store pins corresponding to each note
    note_pins = {}
    
    # object representing 7-segment display
    display = None
    
    # object representing motor
    motor = None
    motor_thread = None
    
    def __init__(self, speaker_0="P1_36", speaker_1="P2_3", speaker_2="P2_1", C="P1_17", D="P1_19", E="P1_21", F="P1_23", G="P1_25", A="P1_27", B="P2_36", i2c_bus=1, i2c_address=0x70, motor="P1_33"):
        # initialize speaker pins
        self.speaker_0 = speaker_0
        self.speaker_1 = speaker_1
        self.speaker_2 = speaker_2

        # initialize note pins
        self.note_pins['A'] = A
        self.note_pins['B'] = B
        self.note_pins['C'] = C
        self.note_pins['D'] = D
        self.note_pins['E'] = E
        self.note_pins['F'] = F
        self.note_pins['G'] = G
        
        # initialize 7-segment display
        self.display = HT16K33.HT16K33(i2c_bus, i2c_address)
        
        # Initialize motor pin
        self.motor = motor
        
        self._setup()
    
    def _setup(self):
        # Initialize Display
        self.set_display_off()
        
        # Initialize Analog Inputs
        ADC.setup()
        
        # Initialize Motor
        self.motor_thread = RunMotor(self.motor)       
        self.motor_thread.start()
        
        # Setup speaker threads into a dictionary
        self.speaker_threads = [PlayNote(self.speaker_0), PlayNote(self.speaker_1), PlayNote(self.speaker_2)]
        for thread in self.speaker_threads:
            thread.start()
            
    
    def run(self):
        # only start running music box if button has been pressed to on
        while(True):
            if music_box_on:
                self.turn_on()
                
                # check each input pin to see if certain notes are being played (need 4 consecutive values to be high)
                on = []
                for note in note_pins.keys():
                    if self.check_threshold(self.note_pins[note]):
                        on.append(Note(note))
                        
                # only take first 3 notes detected
                for i, note in enumerate(on[:3]):
                    self.speaker_threads[i].add_note(note)
                
            else:
                self.turn_off()
    
    def check_threshold(self, pin):
        """
        Checks if an input has hit under threshold voltage (ie. it is toggled on when
        voltage is low enough
        
        Input: analog input pin to check
        Output: true if input has hit threshold voltage
        """
        measured = []
        for i in range(3):
            measured.append(ADC.read_raw(pin))
        return min(measured) <= THRESHOLD
        
    def set_display_on(self):
        """
        Set display to "on"
        """
        self.display.set_digit_raw(0, 0x6F)        # "G"
        self.display.set_digit_raw(1, 0x3F)        # "O"
        self.display.set_digit_raw(2, 0x00)        # " "
        self.display.set_digit_raw(3, 0x00)        # " "
        
    def set_display_off(self):
        """
        Set display to "off"
        """
        self.display.set_digit_raw(0, 0x3F)        # "O"
        self.display.set_digit_raw(1, 0x71)        # "F"
        self.display.set_digit_raw(2, 0x71)        # "F"
        self.display.set_digit_raw(3, 0x00)        # " "
        
    def turn_off(self):
        # set display to off
        self.set_display_off()
        
        # stop motor
        self.motor_thread.pause()
        
    def turn_on(self):
        # set display to on
        self.set_display_on()
        
        # start motor
        self.motor_thread.run()
        
    def cleanup(self):
        """
        Clean up threads
        """
        # Stop speaker threads
        for speaker_thread in self.speaker_threads:
            speaker_thread.end()
        
        # Stop motor thread
        self.motor_thread.end()
        
        # Set Display to show program is complete
        self.display.set_digit(0, 13)        # "D"
        self.display.set_digit(1, 14)        # "E"
        self.display.set_digit(2, 10)        # "A"
        self.display.set_digit(3, 13)        # "D"
        
class BoxButton(threading.Thread):
    button = None
    # False corresponds to off, True corresponds to on
    prev_state = False
    
    def __init__(self, button="P2_2"):
        threading.Thread.__init__(self)
        self.button = button
        
        # Initialize button
        GPIO.setup(self.button, GPIO.IN)
        
    def run(self):
        while not self.stop:
            # check if button is pressed
            if GPIO.input(self.button) == 1:
                # if prev_state was false, then it was just turned on
                if prev_state == False:
                    # previous state now becomes on
                    prev_state = True
                    music_box_on = True
                    
                # if prev_state was true, then it was fjust turned off
                else:
                    prev_state = False
                    music_box_on = False
    
    def end(self):
        """
        Stops thread
        """
        self.stop = True

if __name__ == '__main__':
    box = MusicBox()
    button = BoxButton()
    try:
        box.run()
        button.start
    except KeyboardInterrupt:
        box.cleanup()
        button.end()