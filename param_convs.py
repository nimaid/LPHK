# defines conversion routines for parameters

# int conversion with sensible None handling
def _int(x):
   if x == None or (isinstance(x, str) and x.strip() == ""):
       return 0
   else:
       return int(x)


# float conversion with sensible None handling
def _float(x):
   if x == None or (isinstance(x, str) and x.strip() == ""):
       return 0.0
   else:
       return float(x)


# string conversion with sensible None handling
def _str(x):
   if x == None:
       return ""
   else:
       return x


# no conversion
def _None(x):
   return x