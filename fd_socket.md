ls -l /proc/4650/fd;  lrwx------ 1 men men 64 8月  13 07:26 3 -> 'socket:[58468]'  这个socket:后面的一串数字58468是什么呢？其实是该socket的inode号   static char *sockfs_dname(struct dentry *dentry, char *buffer, int buflen) { return dynamic_dname(dentry, buffer, buflen, "socket:[%lu]", dentry->d_inode->i_ino); }   /proc/net/tcp:sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode         /proc/net/udp  /proc/net/unix              grep 58468 /proc/net/tcp;   13: 0501A8C0:8284 0501A8C0:270F 01 00000000:00000000 00:00000000 00000000  1000        0 58468 1 ffff9c614065a300 20 0 0 10 -1