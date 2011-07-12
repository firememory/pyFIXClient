#!/usr/bin/python3

from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client,  Thread
import random
import time

LOGGER = FIX_Log()

#hostname = '10.6.17.70'
hostname = '127.0.0.1'
#app='trfix'
app='trcap'

if app == 'trfix':
  host = hostname
  port = 9212 
  target = 'MFIXTradeID'
if app == 'trcap':
  host = hostname
  port = 9121
  target = 'MFIXTradeCaptureID'

hertbeat_interval = 0

sender = 'MU0057000001'
#sender = 'MU0057000002'
#sender = 'MU0059000001'

password=' '

##############################################################################################################################
def process_trcap(msg,  self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == '5'):
    sys.exit(0)
  elif (fix.get_tag(msg,  35) == 'A'):
    #network.say Micex::generate_35_D( cl_ord_id, "S01-00000F00", "EQBR", "SBER03", 1, 1, 0, (rand*100).round )
    #8=FIX.4.49=16735=D49=MU005900000156=MFIXTradeCaptureID34=352=20110627-10:56:2911=82750020211=S01-00000F00386=1336=EQBR55=SBER0354=160=20110627-10:56:29.00038=4340=144=010=060
    #trfix
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000)) ), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('54', '1'), ('38', '43'), ('40', '1'),('44', '0') ]) )
    #trcap
    #@network.say Fix::generate_message({ 35 => "AD", 568=> "555", 569=> "0",  263=> "1" })
    msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('49', sender), ('56' , target), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
    self.send(msg)
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('49', sender), ('56' , target), ('568', '444' ), ('569', '0'), ('263',  '1') ]) )
    #self.send(msg)
    #time.sleep(15)
    #logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )
    #self.send(logout_msg)
    
    msg=None
  else:
    msg = None
  return msg


#@network.say Micex::generate_35_D( cl_ord_id_1, "S01-00000F00", "EQBR", "SBER03", 2, 2 , 125, 800, {111=>150} )
##############################################################################################################################
def process_trfix(msg,  self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == 'A'):
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 200), ('40', 2), ('44', 100) , ('111', 50)]) )
    msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 2), ('38', 1000), ('40', 2), ('44', 100) , ('111', 100)]) )
    msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 200), ('40', 2), ('44', 100) , ('111', 50)]) )
    self.send(msg)
    
    time.sleep(30)
    
    msg=None
  else:
    msg = None
  return msg
##############################################################################################################################




if app == 'trfix':
  process = process_trfix
if app == 'trcap':
  process = process_trcap



fix=FIX44()
fix.init(sender , target )
#logon_msg =fix.generate_message ( OrderedDict([('35',  'A'), ('49', sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
hertbeat_interval = 6
logon_msg = fix.generate_Login_35_A(0, ' ',OrderedDict([ ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
#logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )
##############################################################################################################################


def main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)    
    

if __name__ == '__main__':
    main()
