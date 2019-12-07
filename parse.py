# CURRENTLY UNUSED
import parser, types

variables = dict()

def set_var(var_string, val):
    global variables
    try:
        try:
            temp = int(val)
        except:
            temp = float(val)
        variables[var_string] = val
    except:
        if isinstance(val, str):
            value = variables[val]
            variables[var_string] = value

def get_var(var_string):
    try:
        return variables[var_string]
    except:
        return None

def eval_string_and_vars(eq_string, vars_in):
    for var in vars_in:
        eq_string = eq_string.replace(var, str(vars_in[var]))
    eq = parser.expr(eq_string).compile()
    return eval(eq)

def eval_string(eq_string):
    return eval_string_and_vars(eq_string, variables)

def set_var_eval_string(var_string, eq_string):
    global variables
    value = eval_string(eq_string)
    variables[var_string] = str(value)

