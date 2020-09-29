# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2020 <NAME>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - addition
  - subtraction
  - multiplication
  - division

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""
import operator

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def get_user_input():
    """
    Function that prompts users for 2 numbers and an operand to execute on them
    
    Inputs: N/A
    Returns: a tuple containing 2 numbers, and the operation to be executed with them
    """
    op_dict = {'+' : operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '<<': operator.lshift, '>>': operator.rshift, '%': operator.mod, '^': operator.pow}
    
    try:
        num1 = float(input("Enter First Number: "))
        num2 = float(input("Enter Second Number: "))
        op_string = input("Enter operand (+, -, *, /, <<, >>, %, ^): ")
        
        # bitshifts and mod operators can only work if both num1 and num2 are integers
        if (op_string in ['<<', '>>', '%']):
            if (num1.is_integer() and num2.is_integer()):
                num1 = int(num1)
                num2 = int(num2)
            else:
                print("Invalid Input")
                return (None, None, None)
        
        op = op_dict[op_string]
    # check for invalid input
    except:
        print("Invalid Input")
        return (None, None, None)
    
    return (num1, num2, op)


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":
    # make sure we get the correct "input" function based onw hether we are in Python 2 or 3
    try:
        input = raw_input
    except:
        pass
    
    # keep prompting user for a calculation
    while True:
        (num1, num2, op) = get_user_input()
        print(op(num1, num2))