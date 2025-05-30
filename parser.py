import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    'program : stmt_list'
    p[0] = ('program', p[1])

def p_stmt_list_multiple(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2]

def p_stmt_list_single(p):
    'stmt_list : stmt'
    p[0] = [p[1]]

def p_stmt_class(p):
    'stmt : CLASS ID COLON block'
    p[0] = ('class_def', p[2], p[4])

def p_stmt_method(p):
    'stmt : DEF method_name LPAREN param_list RPAREN COLON block'
    p[0] = ('method_def', p[2], p[4], p[7])

def p_stmt_id_stmt(p):
    'stmt : ID attr_chain id_stmt_tail NEWLINE'
    p[0] = ('id_stmt', p[1], p[2], p[3])

def p_stmt_return_expr(p):
    'stmt : RETURN expr NEWLINE'
    p[0] = ('return', p[2])

def p_stmt_return_only(p):
    'stmt : RETURN NEWLINE'
    p[0] = ('return', None)

def p_stmt_pass(p):
    'stmt : PASS NEWLINE'
    p[0] = ('pass',)

#------------------------------------
# NEW

def p_stmt_assignment(p):
    'stmt : term EQUALS term NEWLINE'
    p[0] = ('assignment', p[1], p[3])
#-------------------------------------   
def p_id_stmt_tail_assign(p):
    'id_stmt_tail : EQUALS expr'
    p[0] = ('assign', p[2])

def p_id_stmt_tail_call(p):
    'id_stmt_tail : '
    p[0] = ('method_call',)

def p_method_name_id(p):
    'method_name : ID'
    p[0] = p[1]

def p_method_name_init(p):
    'method_name : INIT'
    p[0] = p[1]

def p_param_list_empty(p):
    'param_list : '
    p[0] = []

def p_param_list_self(p):
    'param_list : SELF'
    p[0] = ['self']

def p_param_list_self_params(p):
    'param_list : SELF COMMA params'
    p[0] = ['self'] + p[3]

def p_param_list_params(p):
    'param_list : params'
    p[0] = p[1]

def p_params_list(p):
    'params : ID COMMA params'
    p[0] = [p[1]] + p[3]

def p_params_single(p):
    'params : ID'
    p[0] = [p[1]]

def p_expr_binary(p):
    'expr : term binary_op term'
    p[0] = ('binary_expr', p[2], p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_id_attr(p):
    'term : ID attr_chain'
    p[0] = ('var', p[1], p[2])

#------------------------
# new

def p_term_self_attr(p):
    'term : SELF DOT ID'
    p[0] = ('self_attr', p[3])

def p_term_id(p):
    'term : ID'
    p[0] = ('id', p[1])
    
#--------------------------
def p_term_number(p):
    'term : NUMBER'
    p[0] = ('number', p[1])

def p_term_string(p):
    'term : STRING'
    p[0] = ('string', p[1])

def p_term_paren(p):
    'term : LPAREN expr RPAREN'
    p[0] = p[2]

def p_binary_op(p):
    '''binary_op : PLUS
                 | MINUS
                 | MUL
                 | DIV'''
    p[0] = p[1]

def p_attr_chain_empty(p):
    'attr_chain : '
    p[0] = []

def p_attr_chain_dot(p):
    'attr_chain : DOT ID attr_chain'
    p[0] = [('dot', p[2])] + p[3]

def p_attr_chain_call(p):
    'attr_chain : LPAREN arg_list RPAREN attr_chain'
    p[0] = [('call', p[2])] + p[4]

def p_arg_list_empty(p):
    'arg_list : '
    p[0] = []

def p_arg_list_multi(p):
    'arg_list : expr COMMA arg_list'
    p[0] = [p[1]] + p[3]

def p_arg_list_single(p):
    'arg_list : expr'
    p[0] = [p[1]]

def p_block(p):
    'block : NEWLINE INDENT stmt_list DEDENT'
    p[0] = p[3]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
