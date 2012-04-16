#! /usr/bin/python

###################################################################################
# Copyright (c) 2012, Alasdair Morrison - www.alasdairmorrison.com
# All rights reserved.
# 
# New BSD License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###################################################################################

# PROBLEM: This could mess up when a new function is implemented (replaces by id)



import MySQLdb, EnigmaSettings
db=EnigmaSettings.mysql_connect()

maximum_number=2000
game_db="64D_mac_new"
missing_function_db="64D_mac__new_missingfunctions"

c=db.cursor()
db.query("""SELECT example, MissingFunctions, NoOfMissingFunctions FROM  """+game_db+""" WHERE example>0 ORDER BY example LIMIT """+str(maximum_number)) #ORDER BY ID DESC

r=db.store_result()
functionHTable={}
try:
 for download_rows in range(0,maximum_number):
    row=r.fetch_row()
    id= row[0][0]
    MissingFunctions = row[0][1]
    NoOfMissingFunctions=row[0][2]

    #Replace the F and U
    #replaced = MissingFunctions.replace("F","").replace("U","").replace("\n",",").replace("\t","").replace(",,","")
    replaced=MissingFunctions
    if replaced=='':
        continue #some games have no missing functions so continue
    functionNames = replaced.split("\n")
    
    
    for function in functionNames:
        functionHTable[function]=functionHTable.get(function,0)+1
except IndexError:
 print "Finished"

print functionHTable
number=0
for functionName,Occurrences in functionHTable.items():
    c.executemany(
          """REPLACE INTO """+missing_function_db+"""
          VALUES (%s, %s, %s)""",

          [(number,functionName,Occurrences)]
          )
    number=number+1

#create table sql
""" CREATE TABLE IF NOT EXISTS `enigma_mac_missingfunctions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `FunctionName` text NOT NULL,
  `Occurrences` int(4) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=458 ; """