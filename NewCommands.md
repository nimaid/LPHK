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

As an example, We'll use the `M_SCROLL` command.   This can be found in the `commands_mouse.py` module.

Recent changes to add variable support to commands has increased the complexity of each command.  Never fear, I have plans to make this even simpler than the previous version, with little to no validation coding needed in the near future.

### Decoding the MOUSE_SCROLL command

The `M_SCROLL` command looks like this:

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
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Scroll amount", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

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
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1
            
        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

        return idx+1


scripts.add_command(Mouse_Scroll())  # register the command
```

We will examine the 5 parts you need to consider

#### Part 1 - The Class Header

Each command is defined as a class.  The Class Header defines that new class, and some of its important properties. 

The class should always begin with some documentation to both highlight the start of the definition of a new class, and also to inform people what the command is supposed to do.  The documentation in this example is minimal rather than optimal.  

```python
# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
```

#### Part 2 - The Class definition

The most important part of the class definition is that the new class is derived from the appropriate base class.  For normal commands, this should be `command_base.Command_Basic` although experienced python programmers could also create a new command definition that derives from another command.

It is also important that you define a unique name for your new command.  I recommend using *Module*_*Command*, where *Module* is the part of the module name after `commands_`.  

```python
class Mouse_Scroll(command_base.Command_Basic):
```

In this example, the `M_SCROLL` command is contained in the `commands_mouse.py` module, so the name of the class should be `Mouse_M_Scroll`, but I've called it `Mouse_Scroll` because every mouse command starts with "M_".  I will probably change this at some point.

#### Part 3 - Class Initialization

The initialization of a command class serves to define the name of the command.  This is literally what you need to place inside your script.

```python
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL")  # the name of the command as you have to enter it in the code
```

Note that commands are case sensitive, so the name should be in all uppercase to be consistent with other commands.

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

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, [1, 2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Scroll amount", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

        return True
```

This may appear more complex than it is.  The first 10 lines are the definition and should simply be copied unchanged into your code.

It is important to note that the validation is called twice, once for the first pass (`pass_no = 1`), and again for the second pass (`pass_no = 2`).  Commands will almost always require some coding in pass 1, and where a command refers to something that may have been defined elsewhere, pass 2 will also be required.

This example has a typical, if simple, pass 1 validation.  This command simply requires that there are 1 or 2 arguments (we check for \[1, 2\]).  Note that in this case, the second parameter is optional

No pass 2 is required for this command.

If errors are to be returned, the correct format is a tuple of 2 strings, the first being the error message, and the second being the line you refer to.  The line referenced is typically (but not always) the line being parsed.  This string is creates automatically by the check_int_param function (that checks for an integer parameter).  By default this function allows a variable to be used, and I have also specified a validation rule.  This validation rule applies to literals.

Finally, the method should return `True` if there were no errors.

The symbol table (`symbols`) is a structure that you need to understand if you are writing more complex commands.

#### Part 5 - Command Execution

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
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
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

#### Part 5 - Command Integration

The final step is to include code to incorporate this command into the set of commands available for scripts.

```python
scripts.add_command(Mouse_Scroll())  # register the command
```

This line creates a command object, and passes it to the routine which adds it to the list of available commands.

It is important to note that the definition of more than one command with exactly the same name will result in only the second one being available.  

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


scripts.add_command(Header_Async())  # register the header
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
                return (self.name + " takes no arguments.", line)

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
scripts.add_command(Header_Async())  # register the header
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
 * 'm_pos' : A tuple containing the saved mouse position
 * 'g_vars' : A tuple containing the lock object and the dictionary of global variables
 * 'l_vars' : A dictionary containing local variables
 * 'stack' : A mutable tuple containing the local stack

The symbol table can be modified in the `Validation` and/or `Run` methods.

An example of adding a new label (from the `GOTO_LABEL` command) is:

```python
            # add label to symbol table                   # Add the new label to the labels in the symbol table
            symbols["labels"][split_line[1]] = idx        # key is label, data is line number
```

This can be checked for existance by:

```python
            if split_line[1] in symbols["labels"]:        # Does the label already exist (that's bad)?
               ...
```

Finally, it can be accessed to determine where a label is:

```python
            return symbols["labels"][split_line[1]]         # normally we return the line number the label is on
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
 * coords[0] - a string describing the location
 * coords[1] - the X value
 * coords[2] - the Y value

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