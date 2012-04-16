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

# This file contains a library of functions used for the other python scripts

__author__="alasdairmorrison"
__date__ ="$Jul 3, 2011 5:49:07 AM$"

import string, urllib2, EnigmaSettings

# globals
Unrecognized_function=0
output_string=0
compiles=0
Unrecognized_function=0
Compile_Succesful=0
segfaulting=0
file_corrupt=0
unknown_error=0
Undefined_symbols_linker=0
multiple_files=0
Resource_name_error=0
Switch_statment=0
REDECLARED_AS_DIFF_SYMBOL=0
ambiguous_overload=0
ISO_ambiguous=0
invalid_operands=0

conversion_error=0
overloaded_ambiguous=0
mouse_enter_leave=0
FOR_error=0
Syntax_error=0
ERROR_404=0

compiler_output=""
db_table=""
missing_functions=""
no_of_missing_functions=0
error_category=""
output_string=""

import subprocess,os

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def run_command(command):
    # Put stderr and stdout into pipes
    proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    stdout = ""
    # Read from pipes
    for line in proc.stdout:
        stdout += line.rstrip()
    stdout += " \n"
    
    for line in proc.stderr:
        stdout+= line.rstrip()
    return stdout


def convert(game):
    global compiler_output,missing_functions, no_of_missing_functions
    startingDir = os.getcwd() # save our current directory

    enigmaDir = EnigmaSettings.getEnigmaDir() 
    os.chdir(enigmaDir) # change to the enigma directory

    print "INFO: The game to give to engima: "+game
    p = os.popen4("java -Xms600M -Xmx600M -jar plugins/LGMUtility.jar \""+game+"\"")

    # pipe the java output to str1
    str1 = p[1].read()
    print "=== start normal output ==="
    print str1[-250:]
    print "=== end normal output ==="
    p[1].close()

    try:
        f= open("redirfile.txt")
        compiler_output=f.read()
        print "=== start of compiler output ==="
        print compiler_output[-500:]
        print "=== end of compiler output ==="
        f.close()
        os.remove("redirfile.txt")
    except Exception, exception:
        compiler_output=""
        print 'exception = ', exception

    try:
        f=open("unimplementedfunctionnames.txt")
        missing_functions=f.read()
        f.close()
        no_of_missing_functions=file_len("unimplementedfunctionnames.txt")-1
        os.remove("unimplementedfunctionnames.txt")
    except Exception, exception:
        missing_functions=""
        no_of_missing_functions=-1
        print 'exception.args = ', exception.args
        print 'exception = ', exception
        
    os.chdir(startingDir) # change back to where we started
    return str1


def get_specific_errors(output):
    global Unrecognized_function,output_string,compiles,Unrecognized_function,Compile_Succesful,segfaulting,file_corrupt,unknown_error,Undefined_symbols_linker,multiple_files, Resource_name_error, Switch_statment, REDECLARED_AS_DIFF_SYMBOL, ambiguous_overload, ISO_ambiguous, invalid_operands
    global conversion_error, overloaded_ambiguous, mouse_enter_leave, FOR_error, Syntax_error, missing_functions, no_of_missing_functions
    global error_category
    output_string=output
    #first do normal output checking for parsing errors
    #important because if parsing doesn't finish the compiler_output file will still be last examples!!!
    if string.find(compiler_output,"make[1]: Nothing to be done for ") !=-1:
        error_category="make[1]: Nothing to be done error"
        Compile_Succesful=0
    elif string.find(output,"Make completed successfully.") !=-1 or string.find(output,"Built to ") !=-1:
        Compile_Succesful=1
        parses=1
        print "Compile succesful! =]"
        error_category="Compile succesful"

    elif string.find(output,"Too few arguments to function") !=-1:
        Unrecognized_function=1
        error_category="Unrecognized function or variable"
    elif string.find(output,"Too many arguments to function") !=-1:
        Unrecognized_function=1
        error_category="Unrecognized function or variable"
    elif string.find(output,"Invalid memory access of location") !=-1:
        segfaulting=1
        error_category="Segfaulting Compiler"
    elif string.find(output,"GM version unsupported or file corrupt") !=-1:
        file_corrupt=1
        error_category="GM version unsupported or file corrupt"
    #elif string.find(output,"java.io.IOException") !=-1:
    #    file_corrupt=1
    #    error_category="Java exception occured (corrupt file?)"
    #elif string.find(output,"Exception in thread ") !=-1:
    #    error_category="Java exception occured!"
    #    unknown_error=1
    elif string.find(output,"Expected ending parenthesis before this point") !=-1:
        FOR_error=1
        error_category="For statement error"
    elif string.find(output,"Goto labels not yet supported") !=-1:
        Switch_statment=1
        error_category="No Switch statement support"
    elif string.find(output,"Syntax error") !=-1:
        Syntax_error=1
        print "Syntax error :("
        error_category="Syntax error"
        # clean up so doesn't write wrong info to mysql
        missing_functions=""
        no_of_missing_functions=0
    #
    #Now do compiler_output checking
    #
    elif string.find(compiler_output,"IDE_EDIT_roomcreates.h:") !=-1:
        unknown_error=1
        error_category="room creation code error (C3)"
    elif string.find(compiler_output,"was not declared in this scope") !=-1:
        Unrecognized_function=1
        print "Unrecognized function or variable :("
        error_category="Unrecognized function or variable"
    elif string.find(compiler_output,"Undefined symbols:") !=-1:
        Undefined_symbols_linker=1
        print "Undefined_symbols linker error :("
        error_category="Undefined_symbols linker error"

    elif string.find(compiler_output,"IDE_EDIT_resourcenames.h") !=-1 or string.find(compiler_output,"error: conflicting declaration") !=-1:
        Resource_name_error=1 #
        error_category="Resource name error"

    elif string.find(compiler_output,"redeclared as different kind of symbol") !=-1:
        REDECLARED_AS_DIFF_SYMBOL=1
        print "Redeclared as different kind of symbol :'("
        error_category="Resource or Variable name error"
    elif string.find(compiler_output,"ambiguous overload for") !=-1:
        ambiguous_overload=1
        error_category="Ambiguous overload error"
    elif string.find(compiler_output,"ISO C++ says that these are ambiguous") !=-1:
        ISO_ambiguous=1
        error_category="Ambiguous error"
    elif string.find(compiler_output,"invalid operands of types") !=-1:
        invalid_operands=1
        error_category="invalid operands"
    elif string.find(compiler_output,"error: conversion from") !=-1 or string.find(compiler_output,"error: invalid conversion from") !=-1:
        conversion_error=1
        error_category="conversion error"
    elif string.find(compiler_output,"call of overloaded") !=-1:
        overloaded_ambiguous=1
        error_category="Ambiguous overload error"
    elif (string.find(compiler_output,"myevent_mouseenter()") !=-1 or string.find(compiler_output,"myevent_mouseleave()") !=-1) and string.find(compiler_output,"was not declared in this scope") !=-1:
        mouse_enter_leave=1
        print "mouse enter/leave error"
        error_category="mouse enter/leave error"
    elif string.find(compiler_output,"error: redeclaration of ") !=-1:
        unknown_error=1
        error_category="redeclaration of var (C5)"
    
    elif string.find(compiler_output,"error: too many arguments to function") !=-1:
        unknown_error=1
        error_category="too many arguments to function (C8)"
    elif string.find(compiler_output,"error: break statement not within loop or switch") !=-1:
        unknown_error=1
        error_category="break statement not within loop or switch (C9)"
    elif string.find(compiler_output," cannot be used as a function") !=-1:
        unknown_error=1
        error_category="action_execute_script without valid script (P1)"
    elif string.find(compiler_output,"error: integer constant is too large for ") !=-1:
        unknown_error=1
        error_category="integer constant is too large! (C17)"
        #
    else:
        unknown_error=1
        #print compiler_output[-1500:]
        error_category="unknown error"
    print "Status: "+error_category


def reset_globals():
    global Unrecognized_function,output_string,compiles,Unrecognized_function,Compile_Succesful,segfaulting,file_corrupt,unknown_error, Undefined_symbols_linker, multiple_files, Resource_name_error, Switch_statment,REDECLARED_AS_DIFF_SYMBOL, ambiguous_overload, ISO_ambiguous, invalid_operands
    global conversion_error, overloaded_ambiguous, mouse_enter_leave, FOR_error, Syntax_error
    global error_category, missing_functions, no_of_missing_functions
    Unrecognized_function=0
    output_string=""
    compiles=0
    Unrecognized_function=0
    Compile_Succesful=0
    segfaulting=0
    file_corrupt=0
    unknown_error=0
    Undefined_symbols_linker=0
    multiple_files=0
    Resource_name_error=0
    Switch_statment=0
    REDECLARED_AS_DIFF_SYMBOL=0
    ambiguous_overload=0
    ISO_ambiguous=0
    invalid_operands=0

    conversion_error=0
    overloaded_ambiguous=0
    mouse_enter_leave=0
    FOR_error=0
    Syntax_error=0
    ERROR_404=0

    compiler_output=""
    error_category=""
    output_string=""
    missing_functions=""
    no_of_missing_functions=-1


def post_data_to_mysql(c,example,name,htmlgamename,db_table,converttime):
    output_for_db=""
    if Compile_Succesful!=1: output_for_db=output_string[-1500:]+"\n ======== compiler output: ============ \n" + compiler_output[-1500:] #only write output if it failed
    c.executemany(
          """REPLACE INTO """+db_table+"""
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",

          [(example,htmlgamename,output_for_db,
          Unrecognized_function,Compile_Succesful,segfaulting,file_corrupt,unknown_error,Undefined_symbols_linker,multiple_files, Resource_name_error, Switch_statment, REDECLARED_AS_DIFF_SYMBOL, ambiguous_overload, ISO_ambiguous, invalid_operands,conversion_error, overloaded_ambiguous, mouse_enter_leave, FOR_error, Syntax_error,error_category,no_of_missing_functions,missing_functions,converttime)]
          )

def post_yyg_data_to_mysql(c,example,db_table):
    print "post_yyg_data_to_mysql"
    c.executemany(
          """UPDATE """+db_table+"""
          SET
          Output_string=%s,
          Unrecognized_function=%s,
          error_category=%s,
          NoOfMissingFunctions=%s,
          MissingFunctions=%s
          WHERE example = %s""",[(output_string[-1500:]+"\n ======== compiler output: ============ \n" + compiler_output[-1500:],
          Unrecognized_function,error_category,no_of_missing_functions,missing_functions,example)]
          )

import os, fnmatch
def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def download(id, url,relativelocation):
    global ERROR_404

    try:
        u = urllib2.urlopen(url)
    except HTTPError:
        print "404!"
        ERROR_404=1
        return ""
    ERROR_404=0 #didn't 404

    if (string.find(url,"64Digits.com")!=-1):
        file_name = url.split('/')[-1]
    else:
        #get the filename
        file_name=u.info()['Content-Disposition']
        file_name=file_name.replace("attachment; filename=\"","").replace("\"","")
        print file_name


    try:
        os.makedirs(relativelocation+str(id)+"/")
    except OSError, exception:
        print "INFO: already exists exc:"+str(exception) #return so it will still convert!
        return relativelocation+str(id)+"/"+file_name


    f = open(relativelocation+str(id)+"/"+file_name, 'w')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += block_sz
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    return relativelocation+str(id)+"/"+file_name


def extract(id,gamefile,relativelocation):
    startingDir = os.getcwd()
    import zipfile
    fullpathToZip = gamefile
    destinationPath = startingDir+relativelocation+str(id)+"/"
    try:
        sourceZip = zipfile.ZipFile(fullpathToZip, 'r')
    except IOError:
        print "file not found"
        return []
    except zipfile.BadZipfile:
        print "bad zip file :/"
        return []
    gmfiles=[]
    for name in sourceZip.namelist():
        if name.find('.exe')!= -1 or name.find('.gmk')!= -1 or name.find('.gmd')!= -1 or name.find('.gm6')!= -1:
            sourceZip.extract(name, destinationPath) #later check for zip files in zip files
            gmfiles.append(destinationPath+name)
        if name.find('.zip') !=-1:
            gmfiles.append(extract(id,destinationPath+name,relativelocation))
            print gmfiles
    sourceZip.close()
    return gmfiles

def createTable(c,tableName):
	print "createtable:"+tableName
	c.execute("""CREATE TABLE IF NOT EXISTS `"""+tableName+"""` (
	  `example` int(11) NOT NULL,
	  `htmlgamename` text NOT NULL,
	  `Output_string` text NOT NULL,
	  `Unrecognized_function` tinyint(1) NOT NULL,
	  `Compile_Succesful` tinyint(1) NOT NULL,
	  `segfaulting` tinyint(1) NOT NULL,
	  `file_corrupt` tinyint(1) NOT NULL,
	  `unknown_error` tinyint(1) NOT NULL,
	  `Undefined_symbols_linker` tinyint(1) NOT NULL,
	  `multiple_files` int(11) NOT NULL,
	  `Resource_name_error` tinyint(1) NOT NULL,
	  `Switch_statment` tinyint(1) NOT NULL,
	  `REDECLARED_AS_DIFF_SYMBOL` tinyint(1) NOT NULL,
	  `ambiguous_overload` tinyint(1) NOT NULL,
	  `ISO_ambiguous` tinyint(1) NOT NULL,
	  `invalid_operands` tinyint(1) NOT NULL,
	  `conversion_error` tinyint(1) NOT NULL,
	  `overloaded_ambiguous` tinyint(1) NOT NULL,
	  `mouse_enter_leave` tinyint(1) NOT NULL,
	  `FOR_error` tinyint(1) NOT NULL,
	  `Syntax_error` int(11) NOT NULL,
	  `error_category` text NOT NULL,
	  `NoOfMissingFunctions` int(5) NOT NULL,
	  `MissingFunctions` text NOT NULL,
      `ConvertTime` text NOT NULL,
	  UNIQUE KEY `example` (`example`)
	) ENGINE=MyISAM DEFAULT CHARSET=latin1;""");