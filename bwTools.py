# vim: nospell
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
import os
import subprocess
import time
from smbus import *

i2bus=SMBus(0)


class bwLCD:

    """
    The method in this class should only be called enclosed with a single
    Lock to avoid concurrency issues
    """
   
    bwTool='/home/vince/bw_rpi_tools/bw_tool/bw_tool -I'
    lcdAddr=00

    def setAddr(lcdAddr):
        lcdAddr=(self.lcdAddr>>1)<<1
        self.lcdAddr=lcdAddr+1

    def clearDisp(self):
        i2bus.write_byte_data(self.lcdAddr,0x10,1)
        return 

    def resetDisp(self):
        i2bus.write_byte_data(self.lcdAddr,0x14,1)
        return 

    def setBacklight(self,perc):
        i2bus.write_byte_data(self.lcdAddr,0x17,255*perc/100.)
        return 
    
    def setContrast(self,perc):
        i2bus.write_byte_data(self.lcdAddr,0x12,255*perc/100.)
        return 


    def setText(self,lineNr,text):
        if lineNr==0:
           posByte=0
        elif lineNr==2:
           posByte=19
        elif lineNr==1:
           posByte=1<<5
        elif lineNr==3:
           posByte=1<<5+19
        i2bus.write_byte_data(self.lcdAddr,0x11,posByte)


        i2bus.write_block_data(self.lcdAddr,0x00,map(lambda
           c:ord(c),text))
        return 
     

class bwDIO:

   """
   The method in this class should only be called enclosed with a single
   Lock to avoid concurrency issues
   """

   bwTool='/home/vince/bw_rpi_tools/bw_tool/bw_tool'
   dioAddr=85

   addString='-D /dev/spidev0.0'

   def setAddr(dioAddr):
      dioAddr=(self.dioAddr>>1)<<1
      self.dioAddr=dioAddr+1

   def setPins(self,pStates):
      runString='%s %s -a %i -r %s -v %i'%(self.bwTool,\
            self.addString,self.dioAddr,0x10,pStates)
      p=subprocess.Popen(runString.split(' '))
      p.wait()
      return

   def setPin(self,pNr,pState):
      runString='%s %s -a %i -r %s -v %i'%(self.bwTool,\
            self.addString,self.dioAddr,0x20+pNr,pState)
      p=subprocess.Popen(runString.split(' '))
      p.wait()
      return

   def setIPins(self):
      dioAddr=(self.dioAddr>>1)<<1
      runString='%s %s -a %i -r 30 -v ff'%(self.bwTool,\
            self.addString,dioAddr)
      p=subprocess.Popen(runString.split(' '))
      p.wait()

   def setIOPins(self,pIOs):
      dioAddr=(self.dioAddr>>1)<<1
      runString='%s %s -a %i -r %s -v %s'%(self.bwTool,\
            self.addString,dioAddr,"30",pIOs)
      p=subprocess.Popen(runString.split(' '))
      p.wait()
      return

   def readID(self):
      dioAddr=self.dioAddr
      runString='%s %s -a %i -i'%(self.bwTool,\
            self.addString,dioAddr)
      p=subprocess.Popen(runString.split(' '),stdout=subprocess.PIPE)
      p.wait()
      return p.stdout.readlines()

   def readPins(self):
      dioAddr=self.dioAddr
      runString='%s %s -a %i -R 10:b'%(self.bwTool,\
            self.addString,dioAddr)
      p=subprocess.Popen(runString.split(' '),stdout=subprocess.PIPE)
      p.wait()
      return int(p.stdout.readlines()[1].strip())

   def readPin(self,pNr):
      dioAddr=self.dioAddr
      runString='%s %s -a %i -R %s:b'%(self.bwTool,\
            self.addString,dioAddr,20+pNr)
      p=subprocess.Popen(runString.split(' '),stdout=subprocess.PIPE)
      p.wait()
      return int(p.stdout.readlines()[1].strip())

if __name__ == "__main__":
   dio=bwDIO()
   dio.setIPins()
   print dio.readPins()
   print dio.readPin(0)
