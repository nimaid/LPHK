import variables


# Constants for auto validation
P_DESCRIPTION    = 0
P_OPTIONAL       = 1
P_VAR_OK         = 2
P_TYPE           = 3
P_CONVERT        = 4
P_P1_VALIDATION  = 5
P_P2_VALIDATION  = 6


# constants for run state
R_INIT     = 0
R_GET      = 1
R_INFO     = 2
R_VALIDATE = 3
R_RUN      = 4
R_FINAL    = 5


# ##################################################
# ### CLASS Command_Basic                        ###
# ##################################################

# Command_Basic is a class that describes a command
class Command_Basic:
    def __init__(
        self, 
        Name: str,          # The name of the command (what you put in the script)
        Lib="LIB_UNSET",
        Auto_validate=None
        ):

        self.name = Name
        self.lib = Lib
        self.auto_validate = Auto_validate
        
        self.valid_max_params = self.Calc_valid_max_params()
        self.valid_num_params = self.Calc_valid_param_counts()

        self.run_states = [R_INIT, R_GET, R_INFO, R_VALIDATE, R_RUN, R_FINAL]
        self.param = None
        self.param_cnt = None            


    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2. For example, goto can be checked on pass 2 to ensure the label
                           # exists
        ):
        
        ret = None
        
        if self.auto_validate:
            if pass_no == 1:
                ret = self.Validate_param_count(ret, idx, line, lines, split_line, symbols, pass_no)        
                ret = self.Validate_params(ret, P_P1_VALIDATION, idx, line, lines, split_line, symbols, pass_no)
 
            if pass_no == 2:
                ret = self.Validate_params(ret, P_P2_VALIDATION, idx, line, lines, split_line, symbols, pass_no)

        if ret == None:
            return ("", "")           # error value!
            
        return ret


    def Parse(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2.  Fatal errors can be generated on pass 1 or 2 for invalid syntax.
                           # Since errors will cause the process to abort, it is permissable for
                           # the same error to be reported on both passes 1 and 2 (since you won't get
                           # past pass 1).
        ):

        ret = self.Validate(idx, line, lines, split_line, symbols, pass_no)
        if ret == True:
            return True 

        if len(ret) != 2:
            ret = ("SYSTEM ERROR PARSING LINE " + str(idx) + ". '" + line + "' on pass " + str(pass_no), line)

        if ret[0]:
            print(ret[0])

        return ret


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        ret = self.Partial_run(idx, split_line, symbols, coords, is_async, self.run_states)

        if ret == -1:
            return ret
        else:
            return idx+1


    def Partial_run(self, idx, split_line, symbols, coords, is_async, run_subset):
        ret = None
        
        try:
            if R_INIT in run_subset:        
                pass
                
            if R_GET in run_subset:        
                ret = self.Run_params(ret, idx, split_line, symbols, coords, is_async, 1)
                if ret == -1:
                    return ret
                
            if R_INFO in run_subset:        
                print("[" + self.Lib + "] " + coords[0] + "  Line:" + str(idx+1) + "     " + self.name + " parameters (" + str(v) + ")")
                
            if R_VALIDATE in run_subset:        
                ret = self.Run_params(ret, idx, split_line, symbols, coords, is_async, 2)
                if ret == -1:
                    return ret
                
            if R_RUN in run_subset:   
                pass        

        finally:        
            if R_FINAL in run_subset:   
                self.param = None
                self.param_cnt = None 

            return ret            
        

    def Calc_valid_max_params(self):
        # Return the maximum number of parameters.  We can calculate this simply based on the number defined
        if self.auto_validate:
            return len(self.auto_validate)
            
        return None


    def Calc_valid_param_counts(self):
        # Return a set of numbers of parameters that are acceptable.  This is defined by which are optional
        ret = None
        
        if self.auto_validate:
            ret = []
            vn = len(self.auto_validate)
            for i in range(vn):
                i_val = self.auto_validate[i]
                if (i_val[P_OPTIONAL] == True) or (i+1 == vn):
                  ret += [i+1]
            
        if ret:
            return set(ret)

        return ret


    def Validate_param_count(self, ret, idx, line, lines, split_line, symbols, pass_no):   
        if not (ret == None or ret == True):
            return ret
            
        if pass_no == 1:
            return variables.Check_num_params(split_line, self.valid_num_params, idx, line, self.name)

        return ret


    def Validate_params(self, ret, val_const, idx, line, lines, split_line, symbols, pass_no):
        if not (ret == None or ret == True):
            return ret
            
        for i in range(self.valid_max_params):
           ret = self.Validate_param_n(ret, i+1, val_const, idx, line, lines, split_line, symbols, pass_no)
           if ret != True:
               return ret

        return ret


    def Validate_param_n(self, ret, n, val_const, idx, line, lines, split_line, symbols, pass_no):
        if not (ret == None or ret == True):
            return ret

        val = self.auto_validate[n-1]
       
        opt = self.valid_num_params == {} or (set(range(1,n)) & self.valid_num_params) != []
                           
        ret = variables.Check_generic_param(split_line, n, val[P_DESCRIPTION], idx, self.name, line, val[P_CONVERT], val[P_TYPE], val[val_const], val[P_OPTIONAL], val[P_VAR_OK])
        if ret == True or ret == None:
            return True
           
        return (ret, line)


    def Run_params(self, ret, idx, split_line, symbols, coords, is_async, pass_no):
        if ret == None:
            ret = True
         
        if pass_no == 1:         
            self.param = [self.name]
            self.param_cnt = len(split_line)

            for i in range(self.valid_max_params):
                if i < self.param_cnt:
                    self.param += [self.Run_param_n(ret, idx, i+1, split_line, symbols, coords, is_async, pass_no)]
                else:
                    self.param += [None]
        elif pass_no == 2:
            for i in range(self.valid_max_params):
                if self.param[i+1] != None:
                    ret = self.Run_param_n(ret, idx, i+1, split_line, symbols, coords, is_async, pass_no)

        return ret


    def Run_param_n(self, ret, idx, n, split_line, symbols, coords, is_async, pass_no):
        if pass_no == 1:
            return variables.get_value(split_line[n], symbols)
        elif pass_no == 2:
            val = self.auto_validate[n-1]
            ok = ret
            
            if val[P_P1_VALIDATION]:
                ok = val[P_P1_VALIDATION](self.param[n], idx, self.name, val[P_DESCRIPTION], n, split_line[n])
                if ok != True:
                    print("[" + self.lib + "] " + coords[0] + "  " + ok)
                    ret = -1
           
        return ret


# ##################################################
# ### CLASS Command_Header                       ###
# ##################################################

# Command_Header is a class specifically defining a header command
class Command_Header(Command_Basic):
 
    def __init__(
        self, 
        Name: str,           # The name of the command (what you put in the script)
        Is_async: bool,      # is this async?
        Lib="LIB_UNSET",
        Auto_validate=None
        ):

        super().__init__(Name, Lib, Auto_validate)
        self.is_async = Is_async

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if idx != 0:
           return ("ERROR on line " + line + ". " + self.name + " must only appear on line 1.", -1)

        return (None, 0)


