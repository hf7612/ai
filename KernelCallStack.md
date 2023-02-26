  kernel什么情况下会调整优先级？ 
  以 set_user_nice 为例 直接看代码和opengrok都挺麻烦,这个静态分析调用堆栈看起来就方便多了.
  一个空格表示一层,后面带！表示没有调用者了.
  从这个分析来看 binder   workq  loop设备   setpriority 会调整优先级，基本就了解哪些场景会触发调整优先级

         set_user_nice
        SYSCALL_DEFINE1_nice!
        binder_do_set_priority
        call_usermodehelper_exec_async!
        create_worker
        khugepaged!
        ksm_scan_thread!
        loop_prepare_queue
        normalize_rt_tasks
        rescuer_thread!
        set_one_prio
        watchdog
       SYSCALL_DEFINE3_setpriority!
       binder_restore_priority
       binder_set_priority
       get_unbound_pool
       loop_set_fd
       maybe_create_worker
       sysrq_handle_unrt!
       task_tick_rt!
       workqueue_init
       workqueue_prepare_cpu!
      alloc_unbound_pwq
      binder_thread_read
      binder_transaction
      binder_transaction_priority
      kernel_init_freeable
      lo_ioctl
      manage_workers
     apply_wqattrs_prepare
     binder_ioctl_write_read
     binder_proc_transaction
     binder_thread_read
     binder_thread_write
     integrity_read_file!
     kernel_init!
     lo_compat_ioctl!
     worker_thread!
     wq_update_unbound_numa
    apply_workqueue_attrs_locked
    binder_ioctl!
    binder_ioctl_write_read
    binder_transaction
    workqueue_apply_unbound_cpumask
    workqueue_init
    workqueue_offline_cpu!
    workqueue_online_cpu!
   apply_workqueue_attrs
   binder_ioctl!
   binder_thread_write
   kernel_init_freeable
   workqueue_set_unbound_cpumask
   wq_cpumask_store!
   wq_nice_store!
   wq_numa_store!
  alloc_and_link_pwqs
  binder_ioctl_write_read
  integrity_read_file!
  kernel_init!
  wq_unbound_cpumask_store!
 __alloc_workqueue_key
 binder_ioctl!
__alloc_workqueue_key!

----------------------------------------------------
![Alt text](KernelCallStack.png?raw=true "Title")


