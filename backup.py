#!/usr/bin/python3
"""
this program is going to  backup files and directories.
if the program run successfully or it failed, it will send two message one through an email and the other one will be saved in a backup.log file.

author: Soha Najmi

email: sohanajmi10@gmail.com 

version: 1.0

"""



import sys
from backupcfg import jobs, dstPath, logPath, smtp  # backupcfg is a python file and we import jobs, dstPath etc from it. basically it mean we linked these two python files.
import os
import pathlib
import shutil
import smtplib
from datetime import datetime

# the logging funcation is going to open a file (backup.log ) and it contain success and failure messages

def logging( message):#Function1 declaration 

    #Function1 definition
    file = open(logPath, "a")
    
    file.write(f"{message}\n") 
   
    file.close()
# the sendEmail funcation is going to send an email from sohanajmi10@gmail.com to 30024957@students.sunitafe.edu.au  with the help of elassticEmail.com server.    
def sendEmail(message):
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'
    
    smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(smtp["user"], smtp["password"])
    smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
    smtp_server.close()
    
# the success function print the message (SUCCESS : BACKUP Done) with date and time 
def success(message, dateTimeStamp):
    print(message, dateTimeStamp)
"""   
    logging(f"'SUCCESS'")
    sendEmail(f"'SUCCESS'")
"""
# the success function print the message (FAILURE : ) with date and time 
def error( errorMessage, dateTimeStamp):
    print(errorMessage, dateTimeStamp) # print error messages on screen
    
    logging(f"FAILURE {errorMessage}, {dateTimeStamp}")   #call the function      #write failurre to log file
    
    sendEmail(f"FAILURE{errorMessage}, {dateTimeStamp}")  # email: errors message to administrator
    
    

def main():
   
    # it print date and time
     dateTimeStamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  
     argCount = len(sys.argv) 
     if argCount != 2: # we need to add or pass at least two argument in command line other wasie it will display the bellow message.
        error("ERROR: job name missing form command line", dateTimeStamp)
        
     else:
          jobName = sys.argv[1] # jobName in here mean the "jobs" in backupcfg or 'jobName = key'. 
         
          if jobName not in jobs:# there are only two jobs in the 'backupcfg.py' job17 and job18. if user type any other jobs than these two. in other word it check for keys, is it typed correctly or not? if not, then it will display the bellow message.
              error(f"ERROR: jobName {jobName} is not defined", dateTimeStamp)
          else:
              #srcPath = jobs[jobName] # here we create a new variable (srcPath).  and we stored  'jobs' value to it. { NOTE: jobs  is a  dictionarie in 'backupcfg.py' }
              for srcPath in jobs[jobName]: # job17 job18
                  if not os.path.exists(srcPath): # here if the source path which is jobs (variable) in  'backupcfg.py'. it check for the value. it should have the correct value. it will display the below message if it is not correct. 
                    error(f"ERROR: Source path {srcPath} does not exit", dateTimeStamp)
                   
                  else:
                    if not os.path.exists(dstPath):# dstPath( destination Path) it hold the address of the backup folder,  which is going to have or stored the copy of files and folders in it. and we defined dstPath in 'backupcfg.py'.
                       error(f"ERROR: des path {dstPath} does not exit", dateTimeStamp)  
                
                    else:
                        srcDetails = pathlib.PurePath(srcPath) # srcDetails has this path '/home/ec2-user/environment/ictprg302/file1.dat'
                       
                        dstLoc = dstPath +  "/" +  srcDetails.name + "-" + dateTimeStamp   #The dstLoc  variable is made by concatenating several strings ('dstPath andsrcDetails'), including a timestamp
                        # dstLoc = f"{dstPath} / {srcDetails.name} -{dateTimeStamp}" # NOTE: this is same as above line.
                       
                        if pathlib.Path(srcPath).is_dir():  # these lines copy the directory or folder
                           shutil.copytree(srcPath, dstLoc)
                           
                        else:
                            shutil.copy2(srcPath, dstLoc) # this one make a copy of files
                            
                           
                        # these three line print the message in backup.log, email and display that terminal   
                        success("SUCCESS: Backup DONE! ", dateTimeStamp)
                        logging(f"SUCCESS: Backup DONE! jobName {jobName} {dateTimeStamp}")
                        sendEmail(f"SUCCESS: Backup DONE!  jobName {jobName} {dateTimeStamp}")

if __name__== '__main__':
    main()
    