高通平台lk流程中对ffbm和recovery优先级处理
从源码分析是
emmc_recovery_init  ->  boot_linux_from_mmc
这两处都是读取misc分区的内容，从而进入不同的模式。
