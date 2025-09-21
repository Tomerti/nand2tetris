"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    arithmetic_commands = 0
    calls = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.filename = ""
        self.function_name = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        CodeWriter.arithmetic_commands += 1

        if command == "add":
            self.__get_last()
            self.__go_second_last()
            self.__write_line("M=M+D")
            self.__decrease()

        elif command == "sub":
            self.__get_last()
            self.__go_second_last()
            self.__write_line("M=M-D")
            self.__decrease()
        elif command == "neg":
            self.__go_last()
            self.__write_line("M=-M")
        elif command == "eq":
            self.__get_last()
            self.__go_second_last()
            self.__write_line("D=M-D")

            self.__write_line(f"@EQ{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JEQ")

            self.__go_second_last()
            self.__write_line("M=0")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            self.__write_line(f"(EQ{CodeWriter.arithmetic_commands})")
            self.__go_second_last()
            self.__write_line("M=-1")
            self.__decrease()

            self.__write_line(f"(END{CodeWriter.arithmetic_commands})")

        elif command == "gt":
            self.__get_second_last()
            self.__write_line(f"@SECONDLASTPOS{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGT")

            ##second last is negative
            self.__get_last()
            self.__write_line(f"@SAMESIGN{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JLT")

            ##second last is negative and last is positive
            self.__get_second_last()
            self.__write_line("M=0")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            # second last is positive
            self.__write_line(f"(SECONDLASTPOS{CodeWriter.arithmetic_commands})")
            self.__get_last()

            self.__write_line(f"@SAMESIGN{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGT")

            # second last is positive and last is negative
            self.__get_second_last()
            self.__write_line("M=-1")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            # both same sign
            self.__write_line(f"(SAMESIGN{CodeWriter.arithmetic_commands})")
            self.__get_second_last()
            self.__go_last()
            self.__write_line("D=D-M")
            self.__write_line(f"@TRUE{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGT")

            self.__get_second_last()
            self.__write_line("M=0")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            self.__write_line(f"(TRUE{CodeWriter.arithmetic_commands})")
            self.__get_second_last()
            self.__write_line("M=-1")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            self.__write_line(f"(END{CodeWriter.arithmetic_commands})")

        elif command == "lt":
            self.__get_second_last()
            self.__write_line(f"@SECONDLASTPOS{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGT")

            ##second last is negative
            self.__get_last()
            self.__write_line(f"@SAMESIGN{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JLT")

            ##second last is negative and last is positive
            self.__get_second_last()
            self.__write_line("M=-1")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            # second last is positive
            self.__write_line(f"(SECONDLASTPOS{CodeWriter.arithmetic_commands})")
            self.__get_last()

            self.__write_line(f"@SAMESIGN{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGT")

            # second last is positive and last is negative
            self.__get_second_last()
            self.__write_line("M=0")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            # both same sign
            self.__write_line(f"(SAMESIGN{CodeWriter.arithmetic_commands})")
            self.__get_second_last()
            self.__go_last()
            self.__write_line("D=D-M")
            self.__write_line(f"@FALSE{CodeWriter.arithmetic_commands}")
            self.__write_line("D;JGE")

            self.__get_second_last()
            self.__write_line("M=-1")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            self.__write_line(f"(FALSE{CodeWriter.arithmetic_commands})")
            self.__get_second_last()
            self.__write_line("M=0")
            self.__decrease()
            self.__write_line(f"@END{CodeWriter.arithmetic_commands}")
            self.__write_line("0;JMP")

            self.__write_line(f"(END{CodeWriter.arithmetic_commands})")

        elif command == "and":
            self.__get_last()
            self.__go_second_last()
            self.__write_line("M=D&M")
            self.__decrease()
        elif command == "or":
            self.__get_last()
            self.__go_second_last()
            self.__write_line("M=D|M")
            self.__decrease()
        elif command == "not":
            self.__go_last()
            self.__write_line("M=!M")
        elif command == "shiftleft":
            self.__go_last()
            self.__write_line("M=M<<")
        elif command == "shiftright":
            self.__go_last()
            self.__write_line("M=M>>")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            if segment in ["local", "argument", "this", "that"]:
                self.__push_segment(segment, index)
            elif segment == "constant":
                self.__push_constant(index)
            elif segment == "static":
                self.__push_static(self.filename, index)
            elif segment == "temp":
                self.__push_temp(index)
            elif segment == "pointer":
                if index == 0:
                    self.__push_pointer("THIS")
                elif index == 1:
                    self.__push_pointer("THAT")
        elif command == "C_POP":
            if segment in ["local", "argument", "this", "that"]:
                self.__pop_segment(segment, index)
            elif segment == "static":
                self.__pop_static(self.filename, index)
            elif segment == "temp":
                self.__pop_temp(index)
            elif segment == "pointer":
                if index == 0:
                    self.__pop_pointer("THIS")
                elif index == 1:
                    self.__pop_pointer("THAT")

    def write_init(self) -> None:
        """Writes the assembly instructions that effect the bootstrap
        code that initializes the VM. This code must be placed at the
        beginning of the generated *.asm file.
        """
        self.__write_line("@256")
        self.__write_line("D=A")
        self.__write_line("@SP")
        self.__write_line("M=D")
        self.write_call("Sys.init", 0)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__write_line(f"({self.function_name}${label})")

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__write_line(f"@{self.function_name}${label}")
        self.__write_line("0;JMP")

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__get_last()
        self.__decrease()
        self.__write_line(f"@{self.function_name}${label}")
        self.__write_line("D;JNE") # jump if not false

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.function_name = function_name
        self.__write_line(f"({self.function_name})")
        for i in range(n_vars):
            self.__push_constant(0)
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        CodeWriter.calls+=1
        self.__write_line(f"@{function_name}$ret.{CodeWriter.calls}")

        self.__write_line("D=A")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()
        self.__push_pointer("LCL")
        self.__push_pointer("ARG")
        self.__push_pointer("THIS")
        self.__push_pointer("THAT")
        self.__write_line("@5")
        self.__write_line("D=A")
        self.__write_line(f"@{n_args}")
        self.__write_line("D=D+A")
        self.__write_line("@SP")
        self.__write_line("D=M-D")
        self.__write_line("@ARG")
        self.__write_line("M=D")
        self.__write_line("@SP")
        self.__write_line("D=M")
        self.__write_line("@LCL")
        self.__write_line("M=D")
        self.__write_line(f"@{function_name}")
        self.__write_line("0;JMP")
        self.__write_line(f"({function_name}$ret.{CodeWriter.calls})")

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.__write_line("@LCL")
        self.__write_line("D=M")
        self.__write_line("@R14")
        self.__write_line("M=D")
        self.__write_line("@5")
        self.__write_line("A=D-A")
        self.__write_line("D=M")
        self.__write_line("@R15")
        self.__write_line("M=D")
        self.__get_last()
        self.__write_line("@ARG")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__decrease()
        self.__write_line("@ARG")
        self.__write_line("D=M")
        self.__write_line("@SP")
        self.__write_line("M=D+1")
        self.__reset_caller("THAT")
        self.__reset_caller("THIS")
        self.__reset_caller("ARG")
        self.__reset_caller("LCL")
        self.__write_line("@R15")
        self.__write_line("A=M")
        self.__write_line("0;JMP")

    def __reset_caller(self,segment:str) -> None:
        if segment == "THAT":
            index = 1
        elif segment == "THIS":
            index = 2
        elif segment == "ARG":
            index = 3
        elif segment == "LCL":
            index = 4
        self.__write_line("@R14")
        self.__write_line("D=M")
        self.__write_line(f"@{index}")
        self.__write_line("D=D-A")
        self.__write_line("A=D")
        self.__write_line("D=M")
        self.__write_line(f"@{segment}")
        self.__write_line("M=D")
    def __pop_pointer(self, segment: str) -> None:
        self.__get_last()
        self.__write_line(f"@{segment}")
        self.__write_line("M=D")
        self.__decrease()

    def __pop_temp(self, index: int) -> None:
        self.__get_last()
        self.__write_line(f"@R{5 + index}")
        self.__write_line("M=D")
        self.__decrease()

    def __pop_static(self, file: str, index: int) -> None:
        self.__get_last()
        self.__write_line(f"@{file.upper()}.{index}")
        self.__write_line("M=D")
        self.__decrease()

    def __pop_segment(self, segment: str, index: int) -> None:
        if segment == "local":
            segment = "LCL"
        elif segment == "argument":
            segment = "ARG"
        elif segment == "this":
            segment = "THIS"
        elif segment == "that":
            segment = "THAT"

        self.__write_line(f"@{segment}")
        self.__write_line("D=M")
        self.__write_line(f"@{index}")
        self.__write_line("D=D+A")
        self.__write_line("@R13")
        self.__write_line("M=D")
        self.__get_last()
        self.__write_line("@R13")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__decrease()

    def __push_pointer(self, segment: str) -> None:
        self.__write_line(f"@{segment}")
        self.__write_line("D=M")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()

    def __push_temp(self, index: int) -> None:
        self.__write_line(f"@R{5 + index}")
        self.__write_line("D=M")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()

    def __push_static(self, file: str, index: int) -> None:
        self.__write_line(f"@{file.upper()}.{index}")
        self.__write_line("D=M")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()

    def __push_constant(self, index: int) -> None:
        self.__write_line(f"@{index}")
        self.__write_line("D=A")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()

    def __push_segment(self, segment: str, index: int) -> None:
        if segment == "local":
            segment = "LCL"
        elif segment == "argument":
            segment = "ARG"
        elif segment == "this":
            segment = "THIS"
        elif segment == "that":
            segment = "THAT"
        self.__write_line(f"@{segment}")
        self.__write_line("D=M")
        self.__write_line(f"@{index}")
        self.__write_line("D=D+A")
        self.__write_line("A=D")
        self.__write_line("D=M")
        self.__write_line("@SP")
        self.__write_line("A=M")
        self.__write_line("M=D")
        self.__increase()

    def __get_last(self) -> None:
        self.__write_line("@SP")
        self.__write_line("A=M-1")
        self.__write_line("D=M")

    def __get_second_last(self) -> None:
        self.__write_line("@SP")
        self.__write_line("A=M-1")
        self.__write_line("A=A-1")
        self.__write_line("D=M")

    def __go_last(self) -> None:
        self.__write_line("@SP")
        self.__write_line("A=M-1")

    def __go_second_last(self) -> None:
        self.__write_line("@SP")
        self.__write_line("A=M-1")
        self.__write_line("A=A-1")

    def __increase(self) -> None:
        self.__write_line("@SP")
        self.__write_line("M=M+1")

    def __decrease(self) -> None:
        self.__write_line("@SP")
        self.__write_line("M=M-1")

    def __write_line(self, line: str) -> None:
        self.output_stream.write(line + "\n")
        return
