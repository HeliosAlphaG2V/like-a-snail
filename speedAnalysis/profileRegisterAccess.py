from _register.lib import registerFlags #@unresolvedImport

#@profile
def doIT():
    return registerFlags.C

for i in range(0, 100000): 
    doIT()