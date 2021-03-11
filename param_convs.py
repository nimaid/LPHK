# defines conversion routines for parameters

# int conversion with sensible None handling
def _int(x):
    if x == None or (isinstance(x, str) and x.strip() == ""):
        return 0
    elif isinstance(x, str):
        x = x.strip()
        try:
            return int(x)
        except:
            try:
                return int(float(x))
            except:
                return 0
    else:
        return int(x)


# float conversion with sensible None handling
def _float(x):
    if x == None or (isinstance(x, str) and x.strip() == ""):
        return 0.0
    elif isinstance(x, str):
        x = x.strip()
        try:
            return float(x)
        except:
            return 0
    else:
        return float(x)


# string conversion with sensible None handling
def _str(x):
    if x == None:
        return ""
    else:
        return str(x)


# no conversion
def _None(x):
    return x


# int conversion with sensible any handling (converts to what we can convert it to)
def _any(x):
    if x == None:
        return 0
    elif isinstance(x, str):
        x = x.strip()
        try:
            return int(x)
        except:
            try:
                return float(x)
            except:
                return 0
    else:
        return str(x)


