#Copyright 2012 Vincent Vandalon
#
#This file is part of AquariumServer. AquariumServer is free software: you can
#redistribute it and/or modify it under the terms of the GNU
#General Public License as published by the Free Software
#Foundation, either version 3 of the License, or (at your
#option) any later version.
#
#AquariumServer is distributed in the hope that it will be
#useful, but WITHOUT ANY WARRANTY; without even the implied
#warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#PURPOSE.  See the GNU General Public License for more
#details.  You should have received a copy of the GNU General
#Public License along with AquariumServer.  If not, see
#<http://www.gnu.org/licenses/>.  
import subprocess

def getTemp(sens):
   if 'ambient' in sens:
      fil=open('/sys/bus/w1/devices/10-000801393f2a/w1_slave')
      olines=fil.readlines()
      fil.close()
      return int((olines[1]).split('=')[1])/1000.
   elif 'reservoir' in sens:
      fil=open('/sys/bus/w1/devices/10-0008028a84f3/w1_slave')
      olines=fil.readlines()
      fil.close()
      return int((olines[1]).split('=')[1])/1000.
   elif 'tank' in sens:
      return 0
      fil=open('/sys/bus/w1/devices/10-0008028a7477/w1_slave')
      olines=fil.readlines()
      fil.close()
      return int((olines[1]).split('=')[1])/1000.
   else:
      return 0
