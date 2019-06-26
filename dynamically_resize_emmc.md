method：
1.compile and produce /data/.qfile_resize2fs,then packed into qpst(or qfile) package.
2.check   /data/.qfile_resize2fs. after system start.
 if exists and unmount /data，
 then resize2fs /dev/block/platform/soc/7824900.sdhci/by-name/userdata
 remove /data/.qfile_resize2fs.
 remount /data
 
 
 end
 
 code exam:
 static int mount_with_alternatives(
 ...
 #define FLAG_RESIZE2FS ".qfile_resize2fs."
 #define MNT_DATA5 "/data"
 if (!strcmp(MNT_DATA5, fstab->recs[i].mount_point)){//if (!strcmp(BLOCK_DATA, fstab->recs[i].blk_device)){ MNT_DATA5
                    if(access(MNT_DATA5 "/" FLAG_RESIZE2FS, F_OK) == 0) { ERROR(" joes found %s \n", MNT_DATA5 "/" FLAG_RESIZE2FS);
                        if (umount(MNT_DATA5) == 0) {
                            system("/system/bin/resize2fs -f /dev/block/platform/soc/7824900.sdhci/by-name/userdata");
                            __mount(fstab->recs[i].blk_device, fstab->recs[i].mount_point, &fstab->recs[i]);
                            unlink(MNT_DATA5 "/" FLAG_RESIZE2FS);
                        }else ERROR(" joes umou fail %s \n", MNT_DATA5);
                    }else ERROR(" joes no %s \n", MNT_DATA5 "/" FLAG_RESIZE2FS);
                }else ERROR(" joes oth dev \n");
                


 
