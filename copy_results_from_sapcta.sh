#!/bin/sh

# See: http://stackoverflow.com/questions/1228466/how-to-filter-files-when-using-scp-to-copy-dir-recursively
rsync  -e ssh -rav --exclude='*/.git/' --exclude='*/utils/' --exclude='*/tests/' --exclude='*/docs/' --exclude='*/datapipe/' --include '*/' --include='*.json' --exclude='*'     sapcta:/home/jdecock/xp/ ./xps/2017_02_23_sapcta/
rsync  -e ssh -rav --exclude='*/.git/' --exclude='*/utils/' --exclude='*/tests/' --exclude='*/docs/' --exclude='*/datapipe/' --include '*/' --include='*.json.log' --exclude='*' sapcta:/home/jdecock/xp/ ./xps/2017_02_23_sapcta/
