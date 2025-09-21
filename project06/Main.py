"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    symbols = SymbolTable()
    first_pass(parser, symbols)
    second_pass(parser, symbols, output_file)


def first_pass(parser: Parser, symbols: SymbolTable) -> None:
    """
    First pass of input file - adds Labels to the symbol table with relevant rom addresses.
    """
    rom_address = 0

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "A_COMMAND" or parser.command_type() == "C_COMMAND":
            rom_address += 1
        else:
            symbols.add_entry(parser.symbol(), rom_address)

    parser.restart()


def second_pass(parser: Parser, symbols: SymbolTable, of: typing.TextIO) -> None:
    """
    second pass of input file - adds Symbols to the symbol table with relevant ram addresses.
    ignores whitespaces and comments, writes every "A" or "C" command to the output file in binary.
    """
    ram_address = [16]

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            continue
        elif parser.command_type() == "A_COMMAND":
            bin_line = fix_a_command(parser, symbols, ram_address)

        elif parser.command_type() == "C_COMMAND":
            bin_line = Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump())
        of.write(bin_line + "\n")


def fix_a_command(parser: Parser, symbols: SymbolTable, ram_address: list[int]) -> str:
    """
    Gets a parser with current "A" command. returns the command address in binary.
    """
    if not parser.symbol().isdecimal():
        if not symbols.contains(parser.symbol()):
            symbols.add_entry(parser.symbol(), ram_address[0])
            ram_address[0] += 1
        command_address = int(symbols.get_address(parser.symbol()))
    else:
        command_address = int(parser.symbol())
    bin_address = bin(command_address)
    bin_address = bin_address.replace("0b", "")
    while len(bin_address) != 16:
        bin_address = "0" + bin_address
    return bin_address


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
