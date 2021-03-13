# Types of commands

There are two major types of commands you may wish to add, these are:
 * Headers
 * Regular commands

In addition, you may also need to review:
 * Registration
 * The Symbol table
 * Coords
 * self.Name
 * Passing Python arguments by reference

In most cases, regular commands will do all you need, and that's probably where you should start.

If you are contemplating adding a new command to an existing module, the process is quite straightforward.  If you are creating a new module to hold your commands, you will also need to refer to the section "Registration".

## Regular Commands

You should make yourself familiar with the way existing commands work.  Look in one of the `commands_*.py` files (other than `commands_header.py`) for examples of existing commands.

You can take advantage of several levels of abstraction when writing your own commands.  Currently there are five obvious options:

 * Declarative definition with *no* coding (Just teasing -- this one doesn't exist yet)
 * Declarative definition, with minimal coding
 * Declarative definition, with manual control over parameter handling
 * Non-declarative definition, with manual coding of parameter handling
 * Completely roll-your-own

### Declarative definition with *no* coding

This is where I'm aiming to get.  You will still need to write some code to perform the actual function, but you can do so by just writing that code, and all the rest is handled for you.  (I'm doing all this work because I'm lazy, and I want you to be able to be lazy too!)

### Declarative definition, with minimal coding

Currently working, this involves declarative definition of the parameters, with manual control over the stages of execution of the Run method.

This has a shorter list of requirements, but it's more coding, and requires more knowledge.

#### Requirements:
 * Declare your parameters
 * Write a basic Run method calling the stages of execution around your output messages and command functionality
 * Register your command

#### Benefits:
 * NO individual Validate method
 * Optional parameters supported
 * Allows use of internally managed numeric variables as well as literal values 
 * Low debugging overhead
 * Easily understandable after viewing limited code
 * Slight risk of maintenance overhead

#### Costs:
 * Parameters must conform to "standard" declarations
 * Required basic understanding of stages of execution of a command 


#### An example - Decoding S_FDIST command

The `S_FDIST` command looks like this:
```python
# ##################################################
# ### CLASS SCRAPE_FINGERPRINT_DISTANCE          ###
# ##################################################

# class that defines the S_FDIST command -- calculates the hamming difference between fingerprints
class Scrape_Fingerprint_Distance(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_FDIST, Calculate the distance between 2 fingerprints",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("F1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("F2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("Distance",   False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    Return the hamming distance between fingerprints {1} and {2} into {3}"), 
            ) )

        self.doc = ["This command calculates the hamming distance between 2 fingerprints.", \
                    "This can be used to determine how similar 2 images are.  The larger", \
                    "the hamming distance, the more different the images are."]


    def Process(self, btn, idx, split_line):
        f1 = self.Get_param(btn, 1)                    # get the fingerprints
        f2 = self.Get_param(btn, 2)
        
        dist = dhash.get_num_bits_different(f1, f2)    # hamming distance (number of bits different)
                    
        self.Set_param(btn, 3, dist)                   # pass the distance back            

        
scripts.Add_command(Scrape_Fingerprint_Distance())  # register the command
```

We will examine the 6 parts you need to consider

##### Part 1 - The Class Header

Each command is defined as a class.  The Class Header defines that new class, and some of its important properties. 

The class should always begin with some documentation to both highlight the start of the definition of a new class, and also to inform people what the command is supposed to do.  The documentation in this example is minimal rather than optimal.  

```python
# ##################################################
# ### CLASS SCRAPE_FINGERPRINT_DISTANCE          ###
# ##################################################

# class that defines the S_FDIST command -- calculates the hamming difference between fingerprints
```

##### Part 2 - The Class definition

The most important part of the class definition is that the new class is derived from the appropriate base class.  For normal commands, this should be `command_base.Command_Basic` although experienced python programmers could also create a new command definition that derives from another command.  Looking at some of the other commands you'll often find a new class defined based on `command_base.Command_Basic` or one of it's derivitives so that common functionality can be made available to all commands derived from it.

It is also important that you define a unique name for your new command.  I recommend using *Module*_*Command*, where *Module* is the part of the module name after `commands_`.  

```python
class Scrape_Fingerprint_Distance(command_base.Command_Basic):
```

##### Part 3 - Class Initialization

The initialization of a command class serves to define the name of the command.  This is also the place you define your parameters.

```python
    def __init__(
        self,
        ):

        super().__init__("S_FDIST, Calculate the distance between 2 fingerprints",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("F1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("F2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("Distance",   False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    Return the hamming distance between fingerprints {1} and {2} into {3}"), 
            ) )

        self.doc = ["This command calculates the hamming distance between 2 fingerprints.", \
                    "This can be used to determine how similar 2 images are.  The larger", \
                    "the hamming distance, the more different the images are."]
```

The 5th line defines the name of the command.  Note that command names are case sensitive, so the name should be in all uppercase to be consistent.  The name can be optionally followed by a comma and a description of the command.  This description is used as part of the auto-documentation of commands

Line 6 passes the name of the current library (lib) to the the object.  The current library will be used to define where the command originates from in some of the low level reporting functions. 

Lines 9 to 11 define the three parameters expected for this function.  Note that this definition actually commences on line 7 with the opening parenthesis and ends on line 12 with the closing parenthesis.  Each parameter is defined by a tuple.

7 values must be entered in each tuple.  The parameters are:
 * The name of the parameter -- this will be used in multiple places to create messages that are understandable.
 * Is this parameter optional? -- Entering True here means that it is valid to pass all the previous parameters, but stop here.  Entering False means that if you have supplied one fewer than this parameter, then you must also supply this one.
 * Can a variable be substituted? - Entering AVV_NO means that only literals are allowed.  AVV_YES means that literals or a variable are permitted.  AVV_REQD means a variable is required.  AVV_REQD is typically used where the command returns or changes the value in this variable.   Note that literal values are validated before execution, variables are validated at execution.
 * What is the type of the parameter -- This is a human-readable description of the datatype required.  It is used in messages, and in validation of literals and variables.
 * Pass 1 Validation - this is a function used to perform pass 1 evaluation of the parameter value.  This will be called at validation for literal values, and at execution for variable values.  Examples of this are variables.Validate_ge_zero, a function that validates a numeric parameter value is greater than or equal to zero.  Use None if no validation is required.  Write your own pass 1 validation routine if you wish!
 * Pass 2 Validation - this is a function called only on pass 2 of the validation.  It is required for commands that reference labels (to determine if the label exists).  None are defined yet, but that will change...

Line 15 contains a skeleton of logging information.  This is a tuple that consists of the number of variables passed, and the format of the message.  In this example it is only valid to pass all three parameters so there is only a single tuple defined.  The magic values '{n}' are replaced by the literal or variable passed to the command.

##### Part 4 - Command Validation

No code is required here!  The default validation code for the class can handle it all for you!

##### Part 5 - Command Execution

```python
    def Process(self, btn, idx, split_line):
        f1 = self.Get_param(btn, 1)                    # get the fingerprints
        f2 = self.Get_param(btn, 2)
        
        dist = dhash.get_num_bits_different(f1, f2)    # hamming distance (number of bits different)
                    
        self.Set_param(btn, 3, dist)                   # pass the distance back            
```

The first line is the standard header and should be copied verbatim.

The parameters are accessed using 'self.Get_param(btn, n)' where 'n' is the parameter number.  This function takes care of both literal values and values passed in variables.  A third (optional) parameter allows you to set a default value if that parameter was not supplied.  It is also possible to use the functions 'self.Param_count(btn)' that returns the number of parameters passed, and 'self.Has_param(btn, n)' to determine if parameter number 'n' has been passed.

Tyically, once the parameters are obtained, the code is inserted to perform the function.  In this case it is a single line calling 'dhash.get_num_bits_different()'

Finally, if there are any parameters to be returned, call 'self.Set_param(btn, n, v)' to return the value 'v' in the nth parameter.  Note that attempting to return values for parameters that are not defined as AVV_REQD will silently fail.

##### Part 6 - Command Integration

The final step is to include code to incorporate this command into the set of commands available for scripts.

```python
scripts.Add_command(Scrape_Fingerprint_Distance())  # register the command
```

This line creates a command object, and passes it to the routine which adds it to the list of available commands.

It is important to note that the definition of more than one command with exactly the same name will result in only the last one being available.  


## DO NOT READ ANY FURTHER IF YOU VALUE YOUR SANITY.  I HAVE TO MAKE THIS EASIER TO UNDERSTAND

There is value (indeed necessity) in using some of these techniques, however many of them are just unneccessary now that I have refined the process of creating commands from their very early implementation.

### Declarative definition, with manual control over parameter handling

More flexible, and required if the variables are not a fixed type (e.g. string followed by a number, or just a number)

#### Requirements:
 * Declare your variables
 * Write a Validate method using the mid-level parameter support functions
 * Write a Run method using the mid-level parameter support functions
 * Register your command

#### Benefits:
 * More flexibility with parameters

#### Costs:
 * More coding required
 * Requires knowledge of the command framework to understand
 * Greater understanding of internal structures needed.
 * Greater probability of introducing bugs and having unexpected behaviour to the command
 * Small risk of maintenance overhead

#### An example - Decoding an old version of the MOUSE_SCROLL command

The `M_SCROLL` command once looked like this:
```python
# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL", (   # the name of the command as you have to enter it in the code
            # Desc            Opt    Var   type  conv  p1_val p2_val 
            ("X value",       False, True, "integer", int, None,  None), \
            ("Scroll amount", False, True, "integer", int, None,  None) ) )

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if not self.auto_validate or len(self.auto_validate) != 2:
            return ("Invalid command setup", btn.line[idx])

        ret = True

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, {1, 2}, idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_numeric_param(split_line, 1, self.auto_validate[1][0], idx, self.name, line, variables.validate_ge_zero, self.auto_validate[1][1], self.auto_validate[1][2])
            if ret != True:
                return (ret, btn.line[idx])

            ret = variables.check_generic_param(split_line, 2, self.auto_validate[1][0], idx, self.name, line, self.auto_validate[1][4], self.auto_validate[1][3], None, False, True)
            if ret != True:
                return (ret, btn.line[idx])

        return ret

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None

        if v2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(v1) + ", " + str(v2) + ")")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(v1))

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X amount", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + btn.coords + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + btn.coords + "  " + ret)
                ok = False

        if not ok:
            return -1

        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

        return idx+1


scripts.Add_command(Mouse_Scroll())  # register the command
```

We will examine the 6 parts you need to consider

##### Part 1 - The Class Header

Each command is defined as a class.  The Class Header defines that new class, and some of its important properties. 

The class should always begin with some documentation to both highlight the start of the definition of a new class, and also to inform people what the command is supposed to do.  The documentation in this example is minimal rather than optimal.  

```python
# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
```

##### Part 2 - The Class definition

The most important part of the class definition is that the new class is derived from the appropriate base class.  For normal commands, this should be `command_base.Command_Basic` although experienced python programmers could also create a new command definition that derives from another command.

It is also important that you define a unique name for your new command.  I recommend using *Module*_*Command*, where *Module* is the part of the module name after `commands_`.  

```python
class Mouse_Scroll(command_base.Command_Basic):
```

##### Part 3 - Class Initialization

The initialization of a command class serves to define the name of the command.  This is literally what you need to place inside your script.

    def __init__(
        self,
        ):

        super().__init__("M_SCROLL", (   # the name of the command as you have to enter it in the code
            # Desc            Opt    Var   type  conv  p1_val p2_val 
            ("X value",       False, True, "integer", int, None,  None), \
            ("Scroll amount", False, True, "integer", int, None,  None) ) )
```

Note that commands are case sensitive, so the name should be in all uppercase to be consistent with other commands.

##### Part 4 - Command Validation

```python
    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if not self.auto_validate or len(self.auto_validate) != 2:
            return ("Invalid command setup", btn.line[idx])

        ret = True

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, {1, 2}, idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_numeric_param(split_line, 1, self.auto_validate[1][0], idx, self.name, line, variables.validate_ge_zero, self.auto_validate[1][1], self.auto_validate[1][2])
            if ret != True:
                return (ret, btn.line[idx])

            ret = variables.check_generic_param(split_line, 2, self.auto_validate[1][0], idx, self.name, line, self.auto_validate[1][4], self.auto_validate[1][3], None, False, True)
            if ret != True:
                return (ret, btn.line[idx])

        return ret
```

##### Part 5 - Command Execution

```python
    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None

        if v2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(v1) + ", " + str(v2) + ")")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(v1))

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X amount", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + btn.coords + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + btn.coords + "  " + ret)
                ok = False

        if not ok:
            return -1

        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

        return idx+1


scripts.Add_command(Mouse_Scroll())  # register the command
```

##### Part 6 - Command Integration

The final step is to include code to incorporate this command into the set of commands available for scripts.

```python
```

This line creates a command object, and passes it to the routine which adds it to the list of available commands.

It is important to note that the definition of more than one command with exactly the same name will result in only the second one being available.  


### Non-declarative definition, with manual coding of parameter handling

#### Requirements:
 * Manual coding of 2 pass Validation method, with support from low level parameter access & validation
 * Manual coding of Run method using low-level variable access and validation.
 * Register your command

#### Benefits:
 * Huge flexibility.
 * Still operates in a standard environment.

#### Costs:
 * Requires detailed knowledge of the command framework to understand
 * Sound understanding of internal structures.
 * Sound understanding of how commands are validated and executed
 * Lots of debugging (but bugs limited to scope of command)
 * Potential maintenance overhead

#### An example - Decoding an old version of the MOUSE_SCROLL command

The `M_SCROLL` command once looked like this:

```python
# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, [1, 2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, btn.line[idx])

            ret = variables.check_int_param(split_line, 2, "Scroll amount", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, btn.line[idx])

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True    
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)
            
        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None
            
        if v2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(v1) + ", " + str(v2) + ")")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(v1))

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X amount", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + btn.coords + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + btn.coords + "  " + ret)
                ok = False

        if not ok:
            return -1
            
        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

        return idx+1


scripts.Add_command(Mouse_Scroll())  # register the command
```

We will examine the 6 parts you need to consider

##### Part 1 - The Class Header

Each command is defined as a class.  The Class Header defines that new class, and some of its important properties. 

The class should always begin with some documentation to both highlight the start of the definition of a new class, and also to inform people what the command is supposed to do.  The documentation in this example is minimal rather than optimal.  

```python
# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
```

##### Part 2 - The Class definition

The most important part of the class definition is that the new class is derived from the appropriate base class.  For normal commands, this should be `command_base.Command_Basic` although experienced python programmers could also create a new command definition that derives from another command.

It is also important that you define a unique name for your new command.  I recommend using *Module*_*Command*, where *Module* is the part of the module name after `commands_`.  

```python
class Mouse_Scroll(command_base.Command_Basic):
```

In this example, the `M_SCROLL` command is contained in the `commands_mouse.py` module, so the name of the class should be `Mouse_M_Scroll`, but I've called it `Mouse_Scroll` because every mouse command starts with "M_".  I will probably change this at some point.

##### Part 3 - Class Initialization

The initialization of a command class serves to define the name of the command.  This is literally what you need to place inside your script.

```python
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL")  # the name of the command as you have to enter it in the code
```

Note that commands are case sensitive, so the name should be in all uppercase to be consistent with other commands.

##### Part 4 - Command Validation

Every command requires a validation.  If you do not provide validation code, the ancestor class will return a blank error message when this command is encountered.

```python
     def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            # check number of split_line
            if len(split_line) != 2:
                return ("Line:" + str(idx+1) + " - Wrong number of parameters in " + self.ame, btn.line[idx])

            try:
                temp = int(split_line[1])
                if variables.valid_var_name(temp):
                
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + " parameter 1 must be a positive number.", btn.line[idx])
            except:
                return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", btn.line[idx])

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, [1, 2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, btn.line[idx])

            ret = variables.check_int_param(split_line, 2, "Scroll amount", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, btn.line[idx])

        return True
```

This may appear more complex than it is.  The first 10 lines are the definition and should simply be copied unchanged into your code.

It is important to note that the validation is called twice, once for the first pass (`pass_no = 1`), and again for the second pass (`pass_no = 2`).  Commands will almost always require some coding in pass 1, and where a command refers to something that may have been defined elsewhere, pass 2 will also be required.

This example has a typical, if simple, pass 1 validation.  This command simply requires that there are 1 or 2 arguments (we check for \[1, 2\]).  Note that in this case, the second parameter is optional

No pass 2 is required for this command.

If errors are to be returned, the correct format is a tuple of 2 strings, the first being the error message, and the second being the line you refer to.  The line referenced is typically (but not always) the line being parsed.  This string is creates automatically by the check_int_param function (that checks for an integer parameter).  By default this function allows a variable to be used, and I have also specified a validation rule.  This validation rule applies to literals.

Finally, the method should return `True` if there were no errors.

The symbol table (`symbols`) is a structure that you need to understand if you are writing more complex commands.

##### Part 5 - Command Execution

Every command that does something (e.g. not labels - that have their effect during pass 1 of validation, or comments - that have no function) requires code to run it.  If you do not provide `Run` code, the ancestor class will do nothing (i.e., it does not generate an error).

```python
    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True    
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)
            
        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None
            
        if v2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(v1) + ", " + str(v2) + ")")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(v1))

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X amount", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + btn.coords + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + btn.coords + "  " + ret)
                ok = False

        if not ok:
            return -1
            
        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

        return idx+1
```

Again, this looks somewhat complex, but isn't really scary.  Again, the first 8 lines are simply the method header and should be copied verbatim.

ok and p are set up to track the success, and store the number of parameters passed respectively.

The variables.get_value function call gets the constant from the command, or the value of a variable if one was specified.  If a parameter is optional (as v2 is here), None will be returned if it does not exist.

Next this command writes an output line describing what it is going to do.   In this case ther are 2 possibilities based on the existance of the second parameter.

The validation code is called again, since variables may have been used.  This does run-time checks of values in a manner similar to the validation that is done earlier for literal values.  It is possible to return multiple errors.

If an error has been detected, the routine exits with -1 indicating failure.

Finally, the work of the function is performed on the validated values.

idx + 1 is returned.  This points to the nect line to execute, which in this instance is the next line (flow control commands may return different values).

##### Part 6 - Command Integration

The final step is to include code to incorporate this command into the set of commands available for scripts.

```python
scripts.Add_command(Mouse_Scroll())  # register the command
```

This line creates a command object, and passes it to the routine which adds it to the list of available commands.

It is important to note that the definition of more than one command with exactly the same name will result in only the second one being available.  

 
### Completely roll-your-own

This requires the most knowledge, creates the possibility of the worst sort of bugs, may be hard to maintain, but is ultimately the most flexible way to add a command because you don't have to follow any rules.

Please consider using an earlier option if you can.

Requirements
 * Expert understanding of LPHK
 * Decisions as to how you will integrate with existing commands
 * Patience

Benefits:
 * Anything goes

Costs:
 * Requires python-fu to understand
 * Potential high maintenance overhead
 * High risk of introducing bugs outside the scope of the current command

### An example?

Sorry, if you're going to roll your own, there is really no model to follow.

## Headers

Headers and Commands are very similar.  The basic format of creating them is the same, however there are some important differences.  This section will concentrate mostly on those differences.

You should make yourself familiar with the way existing headers work.  Look in the `commands_header.py` file for examples of existing commands.

As an example, We'll use the `@ASYNC` header.

Note that this example has not been updated for variable usage.

### Decoding the @ASYNC header

The `@ASYNC` header looks like this:

```python
# ##################################################
# ### CLASS Header_Async                         ###
# ##################################################

class Header_Async(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@ASYNC",      # the name of the header as you have to enter it in the code
            True)                       # You also define if the header causes the script to be asynchronous

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):
        
        if pass_no == 1:
            if idx > 0:        # headers normally have to check the line number
                return (self.name + " must appear on the first line.", lines[0])

            if len(split_line) > 1:
                return (self.name + " takes no arguments.", lines[0])

        return True


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        return idx+1


scripts.Add_command(Header_Async())  # register the header
```

This consists of almost exactly the same 5 parts, but with important differences.

#### Part 1 - The Class Header

This is effectively identical to a regular command.  In this example there is no specific documentation describing what `@ASYNC` actually does -- and that's not good.  You should do better!  

```python
# ##################################################
# ### CLASS Header_Async                         ###
# ##################################################
```

#### Part 2 - The Class definition

The most important part of the class definition is that the new class is derived from the appropriate base class.  For headers, this should be `command_base.Command_Header` although experienced python programmers could also create a new header definition that derives from another header.

The unique name for your header should be derived in a similar way to commands, other than that the leading `@` in a header should be omitted.  (I recommend using *Module*_*Header*, where *Module* is the part of the module name after `commands_`).  

```python
class Header_Async(command_base.Command_Header):
```

In this example, the `@ASYNC` command is contained in the `commands_header.py` module, so the name of the class is `Header_Async`.

#### Part 3 - Class Initialization

The initialization of a header class adds an extra parameter.  You must also specify if this header causes asynchronous behaviour.  Note that headers (by convention) start with `@`.  This is not a requirement, but you should honour it.

```python
    def __init__(
        self, 
        ):

        super().__init__("@ASYNC",      # the name of the header as you have to enter it in the code
            True)                       # You also define if the header causes the script to be asynchronous
```

Note that header names are also case sensitive.

#### Part 4 - Command Validation

Every command requires a validation.  If you do not provide validation code, the ancestor class will return a blank error message when this command is encountered.

```python
    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):
        
        if pass_no == 1:
            if idx > 0:        # headers normally have to check the line number
                return (self.name + " must appear on the first line.", lines[0])

            if len(split_line) > 1:
                return (self.name + " takes no arguments.", btn.line[idx])

        return True
```

Validation for headers is identical to that for commands.  A difference in functionality is that you may want to ensure tha the header is placed in the script in an appropriate place.

It would be quite rare for a header to require second pass validation, but it is still called twice, so it is available if needed.

#### Part 5 - Header Execution

Every command that does something (e.g. not labels - that have their effect during pass 1 of validation, or comments - that have no function) requires code to run it.  If you do not provide `Run` code, the ancestor class will do nothing (i.e., it does not generate an error).

```python
    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        return idx+1
```

The `Run` code for headers is also identical to commands.  

If the header's function is performed during validation (`@ASYNC` is) then there is no need to do anything in the `Run` method.  This is actually the default behaviour, and in this case a `Run` method could be omitted.

#### Part 5 - Command Integration

The final step has the same form, behavior, and cautions as for commands.

```python
scripts.Add_command(Header_Async())  # register the header
```

## Registration

Commands are not dynamically discovered.  This means you need to tell the main executable that a new command module exists.  

In addition, you need to provide an abbreviated name of your module that will be printed in log messages.

### Abbreviated name

This is perhaps the simplest, and you may have already noticed it.  Within each command module a string is defined at the top of that module:

```python
lib = "cmds_ctrl" # name of this library (for logging)
```

For consistency, I recommend you retain the first 5 characters (`cmds_`), and to make the log messages line up, I recommend that the abbreviation is exactly 4 characters (e.g. `midi` for a midi module)  Note that all `lib` strings should be unique.

### Importing the module

The most important step for a new command module is to inform `LPHK.py` of the existance of the new module.  

Edit `command_list.py` to include your new module name.  That's it! 

## The Symbol table

The symbol table is a dictionary of objects passed to `Validate` and `Run` methods that contains important information for the execution of the script.

Currently the dictionary contains x entries:
 * 'repeats' : A dictionary of loop counters for `REPEAT` commands
 * 'original' : A dictionary of the starting values for `REPEAT` commands
 * 'labels' : A dictionary of the label names and locations within the script
 * SYM_MOUSE : A tuple containing the saved mouse position
 * SYM_GLOBAL : A tuple containing the lock object and the dictionary of global variables
 * SYM_LOCAL : A dictionary containing local variables
 * SYM_STACK : A mutable tuple containing the local stack

The symbol table can be modified in the `Validation` and/or `Run` methods.

An example of adding a new label (from the `GOTO_LABEL` command) is:

```python
            # add label to symbol table                   # Add the new label to the labels in the symbol table
            symbols[SYM_LABELS][split_line[1]] = idx        # key is label, data is line number
```

This can be checked for existance by:

```python
            if split_line[1] in symbols[SYM_LABELS]:        # Does the label already exist (that's bad)?
               ...
```

Finally, it can be accessed to determine where a label is:

```python
            return symbols[SYM_LABELS][split_line[1]]         # normally we return the line number the label is on
```

### Repeats

This dictionary within the symbol table contains entries where the key is the line number of the `REPEAT` command, and the value is the number of repeats remaining.

### Original

This dictionary within the symbol table contains entries where the key is the line number of the `REPEAT` command, and the value is the initial value for the number of repeats.

### Labels

This dictionary within the symbol table has entries where the key is the label name, and the value is the line number.

### M_pos

This tuple within the dictionary contains either an empty tuple (`tuple()`) or the saved (x,y) mouse coordinates.

### Global variables

The first element is a lock object used to synchronise access to the global variables.  The second element is a dictionary where the keys are the global variable names and the values are the variable values.

### Local variables

This is a dictionary where the keys are the local variable names and the values are the variable values.

### Stack

This structure contains the list of values that make up the stack for the current command.  Values are added and removed by various "RPN_EVAL" functions.

## Coords

The coords are the current x,y values passed to the command (or header).  I believe these are the button coordinates.

This array contains 3 elements:
 * btn.coords - a string describing the location
 * btn.x - the X value
 * btn.y - the Y value

## self.Name

If an error message needs to refer to the name of the command, using `self.Name` is the preferred method.

## Passing Python arguments by reference

In many programming languages you can pass parameters by value or by reference.  Passing a value by reference allows you to change it in the method and have the value changed in the calling code.  

Python uses a copy on assignment method with parameters passed to a method.  Thus assigning a new value to a parameter does not work

```
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> def change(a):
...   a = 10
...
>>> x = 1
>>> print(x)
1
>>> change(x)
>>> print(x)
1
```

But if you pass a mutable object, you **can** modify it.

```
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> def change(a):
...   a[0] = 10
...
>>> x = [1]
>>> print(x)
[1]
>>> change(x)
>>> print(x)
[10]
```

But you need to be careful to modify it rather than assigning to it, or you'll get the first behaviour

```
(LPHK-build) C:\Users\Steve\Documents\Projects\LPHK\svn-sh\branches\develop>python
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> def change(a):
...   a = [10]
...
>>> x = [1]
>>> print(x)
[1]
>>> change(x)
>>> print(x)
[1]
```

Also, the object passed must be mutable

```
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> def change(a):
...   a[0] = 10
...
>>> x = (1)
>>> change(x)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in change
TypeError: 'int' object does not support item assignment
>>> print(x)
1
```

An advantage of this method is that it allows you to poass constants too.

```
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> def change(a):
...   a[0] = 10
...
>>> change([1])
>>> print([1])
[1]
```

You might wonder why I printed `[1]` in the last example.  This is because a very old historic version of Fortran, if faced with this situation would respond by changing the constant labelled as 1.  This meant that literal constants could be changed at runtime, causing all sorts of weird behaviour!  Python doesn't do that.

For the symbol table I have decided to use a dictionary.  This allows new entries to be added or even removed without changing how otherwise unaffected parts of the code perform.