from time import sleep 
import sys 

for x in range(100): 
    print '\rDownloading: %s (%d%%)' % ("|"*(x/2), x), 
    sys.stdout.flush() 
    sleep(0.1)  
