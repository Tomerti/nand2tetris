// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

@R14
D=M

@mini
M=D

@maxi
M=D

@tempmax
M=0

@tempmin
M=0

@i
M=0
M=M+1

(LOOP)
    @i
    D=M

    @R15
    D=M-D
    @SWAP
    D;JEQ

    @i
    D=M

    @R14
    A=M
    A=A+D
    D=M

    @mini
    A=M
    D=D-M
    @REPLACEMINI
    D;JLT

    (CONT1)
    @i
    D=M

    @R14
    A=M
    A=A+D
    D=M

    @maxi
    A=M
    D=D-M
    @REPLACEMAXI
    D;JGT
    
    (CONT2)
    @i
    M=M+1
    @LOOP
    0;JMP

(REPLACEMIN)
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=A
    @mini
    M=D
    @CONT1
    0;JMP

(REPLACEMAXI)
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=A
    @maxi
    M=D
    @CONT2
    0;JMP

(SWAP)
    @maxi
    A=M
    D=M

    @tempmax
    M=D
    
    @mini
    A=M
    D=M
   
    @tempmin
    M=D
    
    @maxi
    A=M
    M=D
    
    @tempmax
    D=M
    
    @mini
    A=M
    M=D
    

(END)
    @END
    0;JMP