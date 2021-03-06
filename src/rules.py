from codegen.ast import Node
import sys
# META

#start = 'block'

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION'),
    ('left', 'MOD'),
    ('left', 'EQ', 'NEQ', 'LTE','LT','GT','GTE'),
    ('left', 'OR', 'AND'),
)


def p_program_start(t):
	'program : header SEMICOLON block DOT'
	t[0] = Node('program',t[1],t[3])
	print str(t[0])

def p_header(t):
	'header : MODULE identifier'
	t[0] = t[2]
	
def p_block(t):
	"""block : variable_declaration_part function statement_part
	"""
	t[0] = Node('block',t[1],t[2],t[3])
	
	
def p_variable_declaration_part(t):
	"""variable_declaration_part : VARIABLES variable_declaration_list
	 |
	"""
	if len(t) > 1:
		t[0] = t[2]

def p_variable_declaration_list(t):
	"""variable_declaration_list : variable_declaration variable_declaration_list
	 | variable_declaration
	"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('var_list',t[1],t[2])

def p_variable_declaration(t):
	"""variable_declaration : type identifier SEMICOLON"""
	t[0] = Node('var',t[2],t[1]) #node will be as "var_list",identifier, type
	

def p_function(t):
	"""function : function_declaration SEMICOLON function
		| """
		
	if len(t) == 4:
		t[0] = Node('function_list',t[1],t[3])
		

def p_function_declaration(t):
	""" function_declaration : function_heading SEMICOLON block"""
	t[0] = Node('function',t[1],t[3])
	
	
def p_function_heading(t):
	""" function_heading : FUNCTION identifier RETURNS type
		| FUNCTION identifier LPAREN parameter_list RPAREN RETURNS type"""
	if len(t) == 5:
		t[0] = Node("function_head",t[2],t[3])
	else:
		t[0] = Node("function_head",t[2],t[4],t[7])

	
def p_parameter_list(t):
	""" parameter_list : parameter COMMA parameter_list
	| parameter"""
	if len(t) == 4:
		t[0] = Node("parameter_list", t[1], t[3])
	else:
		t[0] = t[1]
		
def p_parameter(t):
	""" parameter : type identifier"""
	t[0] = Node("parameter", t[2], t[1])

def p_type(t):
	""" type : TREAL 
	| TINTEGER
	| TCHAR
	| TSTRING """
	t[0] = Node('type',t[1].lower())
	
def p_statement_part(t):
	"""statement_part : LCURLY statement_sequence RCURLY"""
	t[0] = t[2]
	
def p_statement_sequence(t):
	"""statement_sequence : statement SEMICOLON statement_sequence
	 | statement"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('statement_list',t[1],t[3])
	
def p_statement(t):
	"""statement : assignment_statement
	 | statement_part
	 | if_statement
	 | while_statement
	 | function_call
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]
	
	
def p_function_call(t):
	""" function_call : identifier LPAREN param_list RPAREN
	| identifier """
	
	if len(t) == 2:
		t[0] = Node("function_call", t[1])
	else:
		t[0] = Node("function_call",t[1],t[3])

def p_param_list(t):
	""" param_list : param_list COMMA param
	 | param """
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node("parameter_list",t[1],t[3])

def p_param(t):
	""" param : expression """
	t[0] = Node("parameter",t[1])

	
def p_if_statement(t):
	"""if_statement : IF expression THEN statement ELSE statement
	| IF expression THEN statement
	"""
	
	if len(t) == 5:
		t[0] = Node('if',t[2],t[4])
	else:
		t[0] = Node('if',t[2],t[4],t[6])
	
def p_while_statement(t):
	"""while_statement : WHILE expression DO statement"""
	t[0] = Node('while',t[2],t[4])
	
def p_assignment_statement(t):
	"""assignment_statement : identifier ASSIGNMENT expression"""
	t[0] = Node('assign',t[1],t[3])
	
def p_expression(t):
	"""expression : expression and_or expression_m
	| expression_m
	"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('op',t[2],t[1],t[3])

def p_expression_m(t):
	""" expression_m : expression_s
	| expression_m sign expression_s"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('op',t[2],t[1],t[3])
	
def p_expression_s(t):
	""" expression_s : element 
	| expression_s psign element"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('op',t[2],t[1],t[3])

def p_and_or(t):
	""" and_or : AND
	| OR """
	t[0] = Node('and_or',t[1])

def p_psign(t):
	"""psign : TIMES
	| DIVISION"""
	t[0] = Node('sign',t[1])

def p_sign(t):
	"""sign : PLUS
	| MINUS
	| MOD
	| EQ
	| NEQ
	| LT
	| LTE
	| GT
	| GTE
	"""
	t[0] = Node('sign',t[1])


def p_element(t):
	"""element : identifier
	| real
	| integer
	| string
	| char
	| LPAREN expression RPAREN
	| NOT element
	| function_call_inline
	"""
	if len(t) == 2:
		t[0] = Node("element",t[1])
	elif len(t) == 3:
		# not e
		t[0] = Node('not',t[2])
	else:
		# ( e )
		t[0] = Node('element',t[2])
		
def p_function_call_inline(t):
	""" function_call_inline : identifier LPAREN param_list RPAREN"""
	t[0] = Node('function_call_inline',t[1],t[3])
	
def p_identifier(t):
	""" identifier : IDENTIFIER """
	t[0] = Node('identifier',str(t[1]).lower())
	
def p_real(t):
	""" real : REAL """
	t[0] = Node('real',t[1])
	
def p_integer(t):
	""" integer : INTEGER """
	t[0] = Node('int',t[1])

def p_string(t):
	""" string : STRING """
	t[0] = Node('string',t[1])

def p_char(t):
	""" char : CHAR """
	t[0] = Node('char',t[1])

def p_error(t):
	print "Syntax error in input, in line %d!" % t.lineno
	sys.exit()
