"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        self.jack_tokenizer = input_stream
        self.output = output_stream
        self.classes = ['static', 'field']
        self.subroutines = ['constructor', 'function', 'method']
        self.operations = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
        self.compile_class()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.__write_tag("class")
        self.__multi_generate(3)
        while self.jack_tokenizer.actual_token() in self.classes:
            self.compile_class_var_dec()

        while self.jack_tokenizer.actual_token() in self.subroutines:
            self.compile_subroutine()

        self.__generate()
        self.__write_tag("/class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.__write_tag("classVarDec")
        while self.jack_tokenizer.actual_token() != ";":
            self.__generate()
        self.__generate()
        self.__write_tag("/classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.__write_tag("subroutineDec")
        self.__multi_generate(4)
        self.compile_parameter_list()
        self.__generate()
        self.__write_tag("subroutineBody")
        self.__generate()
        while self.jack_tokenizer.actual_token() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self.__generate()
        self.__write_tag("/subroutineBody")
        self.__write_tag("/subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        # Your code goes here!
        self.__write_tag("parameterList")
        while self.jack_tokenizer.actual_token() != ")":
            self.__generate()
        self.__write_tag("/parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.__write_tag("varDec")
        while self.jack_tokenizer.actual_token() != ";":
            self.__generate()
        self.__generate()
        self.__write_tag("/varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!
        self.__write_tag("statements")
        while (self.jack_tokenizer.actual_token() == "let" or
               self.jack_tokenizer.actual_token() == "if" or
               self.jack_tokenizer.actual_token() == "while" or
               self.jack_tokenizer.actual_token() == "do" or
               self.jack_tokenizer.actual_token() == "return"):
            if self.jack_tokenizer.actual_token() == "let":
                self.compile_let()
            elif self.jack_tokenizer.actual_token() == "if":
                self.compile_if()
            elif self.jack_tokenizer.actual_token() == "while":
                self.compile_while()
            elif self.jack_tokenizer.actual_token() == "do":
                self.compile_do()
            elif self.jack_tokenizer.actual_token() == "return":
                self.compile_return()
        self.__write_tag("/statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.__write_tag("doStatement")
        while self.jack_tokenizer.actual_token() != "(":
            self.__generate()
        self.__generate()
        self.compile_expression_list()
        self.__multi_generate(2)
        self.__write_tag("/doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.__write_tag("letStatement")
        self.__multi_generate(2)
        if self.jack_tokenizer.actual_token() == "[":
            self.__generate_exp_generate()
        self.__generate_exp_generate()
        self.__write_tag("/letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.__write_tag("whileStatement")
        self.__generate()
        self.__generate_exp_generate()
        self.__generate_statement_generate()
        self.__write_tag("/whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.__write_tag("returnStatement")
        self.__generate()
        while self.jack_tokenizer.actual_token() != ';':
            self.compile_expression()
        self.__generate()
        self.__write_tag("/returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.__write_tag("ifStatement")
        while self.jack_tokenizer.actual_token() != "(":
            self.__generate()
        self.__generate_exp_generate()
        self.__generate_statement_generate()
        if self.jack_tokenizer.actual_token() == "else":
            self.__generate()
            self.__generate_statement_generate()
        self.__write_tag("/ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.__write_tag("expression")
        self.compile_term()
        while self.jack_tokenizer.actual_token() in self.operations:
            self.__generate()
            self.compile_term()
        self.__write_tag("/expression")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.__write_tag("term")
        if self.jack_tokenizer.token_type() == "INT_CONST" or self.jack_tokenizer.token_type() == "STRING_CONST":
            self.__generate()
        elif (self.jack_tokenizer.actual_token() == "true" or self.jack_tokenizer.actual_token() == "false"
              or self.jack_tokenizer.actual_token() == "this" or self.jack_tokenizer.actual_token() == "null"):
            self.__generate()
        elif (self.jack_tokenizer.actual_token() == "~" or self.jack_tokenizer.actual_token() == "-"
              or self.jack_tokenizer.actual_token() == "^" or self.jack_tokenizer.actual_token() == "#"):
            self.__generate()
            self.compile_term()
        elif self.jack_tokenizer.token_type() == "IDENTIFIER":
            self.__generate()  # identifier
            if self.jack_tokenizer.actual_token() == "[":
                self.__generate_exp_generate()
            elif self.jack_tokenizer.actual_token() == ".":
                self.__multi_generate(3)
                self.compile_expression_list()
                self.__generate()  # ')' symbol
            elif self.jack_tokenizer.actual_token() == "(":
                self.__generate_exp_generate()
        elif self.jack_tokenizer.actual_token() == "(":
            self.__generate_exp_generate()
        self.__write_tag("/term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.__write_tag("expressionList")
        while self.jack_tokenizer.actual_token() != ")":
            self.compile_expression()
            if self.jack_tokenizer.actual_token() == ",":
                self.__generate()
        self.__write_tag("/expressionList")

    def __generate(self):
        token_type = self.jack_tokenizer.token_type()
        if token_type == "KEYWORD":
            token_type = "keyword"
            token_data = self.jack_tokenizer.keyword().lower()
        elif token_type == "SYMBOL":
            token_type = "symbol"
            token_data = self.jack_tokenizer.symbol()
            if token_data == '&':
                token_data = "&amp;"
            elif token_data == '>':
                token_data = "&gt;"
            elif token_data == '<':
                token_data = "&lt;"
        elif token_type == "INT_CONST":
            token_type = "integerConstant"
            token_data = self.jack_tokenizer.int_val()
        elif token_type == "STRING_CONST":
            token_type = "stringConstant"
            token_data = self.jack_tokenizer.string_val()
        else:
            token_type = "identifier"
            token_data = self.jack_tokenizer.identifier()
        token = "<" + token_type + "> " + str(token_data) + " </" + token_type + ">\n"
        self.jack_tokenizer.advance()
        self.output.write(token)

    def __write_tag(self, segment):
        self.output.write("<" + segment + ">\n")

    def __generate_exp_generate(self):
        self.__generate()
        self.compile_expression()
        self.__generate()

    def __generate_statement_generate(self):
        self.__generate()
        self.compile_statements()
        self.__generate()

    def __multi_generate(self, repeats):
        for i in range(repeats):
            self.__generate()
