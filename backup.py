#!/usr/bin/python3

import sys
from backupcfg import jobs, dstPath  # backupcfg is a python file and we import from it jobs and dstPath basically mean we linked these two python files
import os
import pathlib
import shutil
from datetime import datetime

def main():
    # date and time
     dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")  
     argCount = len(sys.argv) 
     if argCount != 2: # we need to add at pass at least to argument in command line other wasie it will display the bellow message. 
          print("ERROR: job name missing form command line")
     else:
          jobName = sys.argv[1] # jobName in here mean the "jobs" in backupcfg or 'jobName = key'. 
         
          if jobName not in jobs:# there are only two jobs in the 'backupcfg.py' job17 and job18. if user type any other jobs than these two. in other word it check for keys, is it typed correctly or not? if not, then it will display the bellow message.
              print(f"ERROR: jobName {jobName} is not defined")
          else:
              srcPath = jobs[jobName] # here we create a new variable (srcPath).  and we stored  'jobs' value to it. { NOTE: jobs  is a  dictionarie in 'backupcfg.py' }
              if not os.path.exists(srcPath): # here if the source path which is jobs (variable) in  'backupcfg.py'. it check for the value. it should have the correct value. it will display the below message if it is not correct. 
                  print(f"ERROR: Source path {srcPath} does not exit")
              else:
                   if not os.path.exists(dstPath):# dstPath( destination Path) it hold the address of the backup folder,  which is going to have or stored the copy of files and folders in it. and we defined dstPath in 'backupcfg.py'.
                       print(f"ERROR: des path {dstPath} does not exit")
                   else:
                       
                       srcDetails = pathlib.PurePath(srcPath) #???????????
                       
                       dstLoc = dstPath +  "/" +  srcDetails.name + "-" + dateTimeStamp   #????????????
                       
                       if pathlib.Path(srcPath).is_dir():  # these lines copy the directory or folder
                           shutil.copytree(srcPath, dstLoc)
                       else:
                           shutil.copy2(srcPath, dstLoc) # this one make a copy of files
                           pass
                           
                           
  

if __name__== '__main__':
    main()