android mount file (system userdata cache)的分析
在 device/qcom/msm8953_64/init.target.rc
 on fs
      wait /dev/block/bootdevice
      mount_all fstab.qcom

system/core/init/builtins.cpp
  static const Map builtin_functions = {
  ...
  {"mount_all",               {1,     kMax, do_mount_all}},
  ...
  };
   ...
  static int do_mount_all(const std::vector<std::string>& args){
  ...
  int ret =  mount_fstab(fstabfile, mount_mode);
  ...
  }
  
  static int mount_fstab(const char* fstabfile, int mount_mode) {
  ...
  child_ret = fs_mgr_mount_all(fstab2, mount_mode);
  ...
  }
  
  system/core/fs_mgr/fs_mgr.c
  int fs_mgr_mount_all(struct fstab *fstab, int mount_mode) {
  ...
  mret = mount_with_alternatives(fstab, i, &last_idx_inspected, &attempted_idx);
  ..
  }
  
  static int mount_with_alternatives(struct fstab *fstab, int start_idx, int *end_idx, int *attempted_idx) {
  ...
  if (!__mount(fstab->recs[i].blk_device, fstab->recs[i].mount_point, &fstab->recs[i])) {
  ...
  }
  
  static int __mount(const char *source, const char *target, const struct fstab_rec *rec) {
  ...
  ret = mount(source, target, rec->fs_type, mountflags, rec->fs_options);
  ...
  }
  
  完
