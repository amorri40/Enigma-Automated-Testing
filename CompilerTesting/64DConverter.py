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

if __name__ == "__main__":
    print "============ Starting Converting ============";

#modes
minimum_example=780
maximum_number=2 #number of games to convert

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

from urllib2 import HTTPError
import urllib2,os, string, sys, datetime, calendar, time, getopt
from BeautifulSoup import BeautifulSoup, SoupStrainer
import ConvertingEnigma, EnigmaSettings

g_start = time.time()
g_compileForWindows=False

db=EnigmaSettings.mysql_connect()
c=db.cursor()
print "INFO: connected to mysql successfully"


if len(sys.argv) < 3:  # the program name and the two arguments
  # stop the program and print an error message
  sys.exit("Must provide, 1) example id to start from 2) number of examples from that id to convert")



optlist, args = getopt.getopt(sys.argv[1:], 'w',['windows'])
print optlist
print args

#get the command line args
minimum_example = int(args[0])-1
maximum_number = int(args[1])

for o, a in optlist:
        if o == "--windows" or o == "-w":
            g_compileForWindows = True


#
def compile_mingw():
    build_dir=EnigmaSettings.getEnigmaDir()#+"/ENIGMASystem/SHELL/"
    cwd = os.getcwd() # get current directory
    try:
       os.chdir(build_dir)
       return ConvertingEnigma.run_command("make Game GMODE=Run GRAPHICS=OpenGL AUDIO=None COLLISION=BBox WIDGETS=None PLATFORM=Win32 CXX=\"/usr/local/i386-mingw32-4.3.0/bin/i386-mingw32-g++ -Wfatal-errors -w -I./Platforms/Win32/ffi -I./../additional/zlib -L./Platforms/Win32/ffi -L./../additional/zlib\" CC=\"/usr/local/i386-mingw32-4.3.0/bin/i386-mingw32-gcc -Wfatal-errors -w\" COMPILEPATH=MacOSX/Windows EXTENSIONS=\"Universal_System/Extensions/Alarms Universal_System/Extensions/Timelines Universal_System/Extensions/Paths Universal_System/Extensions/MotionPlanning Universal_System/Extensions/Unimplemented Universal_System/Extensions/DateTime Universal_System/Extensions/DataStructures\" OUTPUTNAME=\"/Users/alasdairmorrison/Enigma/Enigma_clean_April_2012/EnigmaXcode.exe\"")
    finally:
      os.chdir(cwd)
    

now = datetime.datetime.now()
g_platform=sys.platform
#create the table for this revision if not already created
db_table="64D_"+g_platform+"__"+calendar.month_abbr[now.month]+str(now.year)
ConvertingEnigma.createTable(c,db_table)
if g_compileForWindows==True: g_windowsTable="64D_win32__"+calendar.month_abbr[now.month]+str(now.year); ConvertingEnigma.createTable(c,g_windowsTable)

#start
startingDir = os.getcwd()
db.query("""SELECT ID, Name, SiteLink, DownloadLink FROM GameDetails WHERE ID>"""+str(minimum_example)+""" ORDER BY ID LIMIT """+str(maximum_number)) #ORDER BY ID DESC

r=db.store_result()
for download_rows in range(0,maximum_number):
    game_start_time = time.time()
    row=r.fetch_row()
    url= row[0][3]
    id= row[0][0]
    name = row[0][1]
    sitelink=row[0][2]
    print "==================================="
    print "============== "+str(id)+" ("+str(download_rows)+" of "+str(maximum_number)+") ============= "
    print "==================================="
    

#first find if gmk is already downloaded
    gmks=ConvertingEnigma.locate('*.gm*',startingDir+"/../examples/"+str(id)+"/")
    gmfiles= list(gmks)
    if len(gmfiles)>0:
        print "INFO: Found GM files!"
        print gmfiles
    else:
     print "INFO: No gmk files, Time to download..."
     try:

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)

        tags = soup.findAll('a', style="color: #1a058b;")
        downlink= tags[0]['href']
        print "INFO: Download link:"+downlink

        game=ConvertingEnigma.download(id,"http://64Digits.com/"+downlink,"../examples/")
        print "INFO: game name:"+game
        if ERROR_404==1:
            ConvertingEnigma.reset_globals()
            print "ERROR: 404 not found!"
            continue

        gmfiles = []
        
        if string.find(game.lower(),".zip") !=-1: #if game ends with .zip
            gmfiles=ConvertingEnigma.extract(id,game,"/../examples/")#startingDir+game)
        
        elif string.find(game,".rar") !=-1: #if rar file
         print "ERROR: Rar file!"
         continue

        elif game.find('.gmk')!= -1 or game.find('.gmd')!= -1 or game.find('.gm6')!= -1: #already a gm source file
            gmfiles.append(startingDir+"/"+game)

        else:
            print "ERROR: Not a game maker file!"

     except Exception, exception:
         print "ERROR: 64Digits probably down: " +str(exception)
         continue;

    multiple_files=len(gmfiles)
    if multiple_files >0:
        for gmfile in gmfiles:
            #print "INFO: The game maker file "+gmfile
            output=ConvertingEnigma.convert(gmfile)
            ConvertingEnigma.get_specific_errors(output)
    converttime=(time.time() - game_start_time)
    htmlgamename = "<a href=\"http://64digits.com/games/"+sitelink+"\">"+name+"</a>"
    ConvertingEnigma.post_data_to_mysql(c,str(id),name,htmlgamename,db_table,str(converttime))
    compile_succesful=ConvertingEnigma.Compile_Succesful #used later on to check if its worth compiling to other platform
    ConvertingEnigma.reset_globals()
    #now windows:
    if g_compileForWindows and compile_succesful == 1: 
        winoutput=compile_mingw() #compiles last game to windows (may want to remove)
        print "=== WINDOWS OUTPUT ==="
        print winoutput[-250:]
        print "= END WINDOWS OUTPUT ="
        windowstime=(time.time() - game_start_time)-converttime
        ConvertingEnigma.get_specific_errors(winoutput)
        ConvertingEnigma.post_data_to_mysql(c,str(id),name,htmlgamename,g_windowsTable,str(windowstime))
        ConvertingEnigma.reset_globals()
        print "windows time:"+str(windowstime)+" seconds"
        
    
    print "overall elapsed ="+ str(time.time() - game_start_time)
print "total elapsed ="+ str(time.time() - g_start)+" seconds"    
            
    