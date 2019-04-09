#!/usr/bin/python
import os, sys
from stat import *
def walktree(top, callback):
    '''recursively descend the directory tree rooted at top, calling the ca llback function for each regular file'''
    for f in os.listdir(top):
        pathname = os.path.join(top, f) # print pathname
        try:
            mode = os.stat(pathname).st_mode        
            if S_ISDIR(mode): # It's a directory, recurse into it
                walktree(pathname, callback)
            elif S_ISREG(mode): # It's a file, call the ca llback function            
                ati = os.stat(pathname).st_atime
                mti = os.stat(pathname).st_mtime
                if ati!=mti:
                    callback(pathname)
            # else: # Unknown file type, print a message      stat.ST_ATIME   stat.ST_MTIME   stat.S_ISREG ; #print 'Skipping %s' % pathname
        except OSError:
            pass #continue; #nop # print ' '

def visitfile(file):    
    print file #print 'visiting', file
if __name__ == '__main__':
    walktree(sys.argv[1], visitfile)
