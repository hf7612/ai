恢复出厂设置流程：

packages/apps/Settings/src/com/android/settings/MasterClearConfirm.java：
发送 Intent.ACTION_MASTER_CLEAR 广播

frameworks/base/core/java/android/os/RecoverySystem.java
调用 
rebootWipeUserData

再到
frameworks/base/services/core/java/com/android/server/RecoverySystemService.java
rebootRecoveryWithCommand
setupOrClearBcb
SystemProperties.set("ctl.start", "setup-bcb");

再启动
bootable/recovery/uncrypt/uncrypt.cpp
setup_bcb

最后是frameworks/base/services/core/java/com/android/server/RecoverySystemService.java
pm.reboot(PowerManager.REBOOT_RECOVERY);

注意广播：
frameworks/base/core/res/AndroidManifest.xml
  receiver android:name="com.android.server.MasterClearReceiver" 
  action android:name="android.intent.action.MASTER_CLEAR" 
