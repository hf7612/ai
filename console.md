在android和嵌入式开发中串口log非常重要，在分析一些稳定性问题是需要理顺console. 在一次开发中为了验证vold的功能，特意将vold删掉，结果系统卡住，串口也无法输入， 为了不影响后面的调试，需要解决串口输入。 花了几分钟简单分析了下 system/core/rootdir/init.rc

service console /system/bin/sh 

class core console  

disabled 

 user shell group shell log readproc 

 seclabel u:rshells0 

 on property:ro.debuggable=1 

 chmod 0773 /data/misc/trace 

 start console

按理 ro.debuggable 这个属性已经是1了，但在死机情况下无法得到求证。 从log看 logd已经是起来的了

 然后在下面加上 start console

on post-fs

start console

 start logd 
 
 重启机器，问题解决，串口也能输入，ok！
