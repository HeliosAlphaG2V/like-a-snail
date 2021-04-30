'''
Created on 02.05.2019

@author: Admin
'''
from _registerFlags.lib import registerFlags #@unresolvedImport

@profile
def doIT():
    return registerFlags.C

for i in range(0, 100000): 
    doIT()