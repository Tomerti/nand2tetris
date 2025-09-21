"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if mnemonic == None:
            return "000"
        elif mnemonic == "M":
            return "001"
        elif mnemonic == "D":
            return "010"
        elif mnemonic == "MD":
            return "011"
        elif mnemonic == "A":
            return "100"
        elif mnemonic == "AM":
            return "101"
        elif mnemonic == "AD":
            return "110"
        elif mnemonic == "AMD":
            return "111"


    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        if mnemonic == "0":
            return "1110101010"
        elif mnemonic == "1":
            return "1110111111"
        elif mnemonic == "-1":
            return "1110111010"
        elif mnemonic == "D":
            return "1110001100"
        elif mnemonic == "A":
            return "1110110000"
        elif mnemonic == "M":
            return "1111110000"
        elif mnemonic == "!D":
            return "1110001101"
        elif mnemonic == "!A":
            return "1110110001"
        elif mnemonic == "!M":
            return "1111110001"
        elif mnemonic == "-D":
            return "1110001111"
        elif mnemonic == "-A":
            return "1110110011"
        elif mnemonic == "-M":
            return "1111110011"
        elif mnemonic == "D+1":
            return "1110011111"
        elif mnemonic == "A+1":
            return "1110110111"
        elif mnemonic == "M+1":
            return "1111110111"
        elif mnemonic == "D-1":
            return "1110001110"
        elif mnemonic == "A-1":
            return "1110110010"
        elif mnemonic == "M-1":
            return "1111110010"
        elif mnemonic == "D+A":
            return "1110000010"
        elif mnemonic == "D+M":
            return "1111000010"
        elif mnemonic == "D-A":
            return "1110010011"
        elif mnemonic == "D-M":
            return "1111010011"
        elif mnemonic == "A-D":
            return "1110000111"
        elif mnemonic == "M-D":
            return "1111000111"
        elif mnemonic == "D&A":
            return "1110000000"
        elif mnemonic == "D&M":
            return "1111000000"
        elif mnemonic == "D|A":
            return "1110010101"
        elif mnemonic == "D|M":
            return "1111010101"
        elif mnemonic == "A<<":
            return "1010100000"
        elif mnemonic == "D<<":
            return "1010110000"
        elif mnemonic == "M<<":
            return "1011100000"
        elif mnemonic == "A>>":
            return "1010000000"
        elif mnemonic == "D>>":
            return "1010010000"
        elif mnemonic == "M>>":
            return "1011000000"



    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if mnemonic == None:
            return "000"
        elif mnemonic == "JGT":
            return "001"
        elif mnemonic == "JEQ":
            return "010"
        elif mnemonic == "JGE":
            return "011"
        elif mnemonic == "JLT":
            return "100"
        elif mnemonic == "JNE":
            return "101"
        elif mnemonic == "JLE":
            return "110"
        elif mnemonic == "JMP":
            return "111"
