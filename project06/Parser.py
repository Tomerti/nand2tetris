"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import string
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_lines = input_file.read().splitlines()
        self.current_command = None
        self.current_line_number = -1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        for i in range(self.current_line_number + 1, len(self.input_lines)):
            if self.valid_command(self.input_lines[i]):
                return True
        return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        for i in range(self.current_line_number + 1, len(self.input_lines)):
            self.current_line_number = i
            if self.valid_command(self.input_lines[i]):
                self.current_command = self.input_lines[i].replace(" ", "").split("//")[0]
                return None

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if "@" in self.current_command:
            return "A_COMMAND"
        if "(" in self.current_command:
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        return self.current_command.translate(str.maketrans('', '', "(@)"))

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        dest = self.current_command.split("=")
        if len(dest) == 1:
            return None
        return dest[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        comp = self.current_command.split("=")

        if len(comp) == 1:
            return comp[0].split(";")[0]
        return comp[1].split(";")[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        jump = self.current_command.split(";")

        if len(jump) == 1:
            return None
        return jump[1]

    def valid_command(self, line: str) -> bool:
        """
        checks if given line is a valid command.
        """
        line = line.replace(" ", "")
        if line.startswith("//") or line == "\n" or line == "\r" or not line:
            return False
        return True

    def restart(self) -> None:
        """
        restarts the parser to default values
        """
        self.current_command = None
        self.current_line_number = -1
