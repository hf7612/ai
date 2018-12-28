#!/usr/bin/python
#  split  raw dump form partition to QPST dump format either full dump or minidump
#
import sys
import os
import getopt
import time
import glob
import re
import string
import struct
import subprocess

try:
    from gen_html import *
except ImportError, e:
    print e, "Skip.."

class minidump():

    diag_dict = {}
    out_folder = '.'
    out_file = None
    hw_id = '660'
    symbol = {}

    def print_output(self, string):
        self.out_file.write(string + "\n")

    def open_file(self, name, op):
        path = os.path.join(self.out_folder, name)
        self.out_file = open(path, op)
        return self.out_file

    def extract_kaslr_offset(self, f, offset, size, outfile ):
        while True:
            f.seek(offset)
            buf = f.read(12)
            if len(buf) < 4:
                break;
            offset += 4
            (magic, kaslr) = struct.unpack_from("<IQ", buf, 0)
            if magic == 0xdead4ead:
                break;
        if magic != 0xdead4ead:
            print("Does not found Magic 0xdead4ead for kaslr_offset")
            return 0
        print("Found IMEM kaslr_offset=0x{:<x}".format(kaslr))
        if outfile != '':
            print("Generating trace32 cmm %s" % outfile)
            fo = self.open_file(outfile,"w")
            fo.write("d.load.elf ap_minidump.elf /logload\n")
            fo.write("d.load.elf vmlinux 0x{:x} /noclear\n".format(kaslr))
            fo.close()
        return kaslr

    def get_vmlinux_path(self):
        if os.path.exists("vmlinux"):
            return "vmlinux"
        elif os.path.exists(os.path.join("..", "vmlinux")):
            return os.path.join("..", "vmlinux")
        else:
            return ''

    def check_banner(self, sbldump):
        out = os.popen("strings {}|grep 'Linux version' ".format(sbldump))
        for line2 in out.read().split('\n'):
            line2 = line2.strip('"')
            print("sbldump:{}".format(line2))
        
        vmlinux = self.get_vmlinux_path()
        if vmlinux == '':
            print "no vmlinux found"
            return
        out = os.popen("strings {}|grep 'Linux version' ".format(vmlinux))
        for line1 in out.read().split('\n'):
            print("vmlinux:{}".format(line1))
            break
        if line1 == line2:
            print "vmlinux match"
        else:
            print "vmlinux not match"


    def get_kaslr_offset(self):
        vmlinux = self.get_vmlinux_path()
        if vmlinux == '':
            print "no vmlinux found"
            vm_vaddr = 0
        else:
            vm_vaddr = self.vmlinux_symbol(vmlinux, "linux_banner") 
        r_vaddr = self.elf_segment_vaddr("md_KELF_HEADER.BIN", "linux_banner")
        print "kelf:{:x} -  vmlinux:{:x} = {:x}".format(r_vaddr, vm_vaddr, r_vaddr - vm_vaddr)
        return r_vaddr-vm_vaddr

    def elf_segment_vaddr(self, elf, seg_name):
        elf = os.path.join(self.out_folder, elf)
        readelf_out = subprocess.Popen(
            ["readelf", '-S', elf],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        found = False
        while True:
            line = readelf_out.stdout.readline().rstrip('\r\n')
            if re.search(seg_name, line):
                found = True
            s = re.search("PROGBITS\s+(\S+)", line)
            if found and s:
                vaddr = int(s.group(1), 16)
                return vaddr
            if readelf_out.poll():
                print line
                break
        return 0

    def vmlinux_symbol(self, vmlinux, symbol):
        nm_out = os.popen("nm -p {} ".format(vmlinux, symbol))
        f_vaddr = 0
        for line in nm_out.read().split('\n'):
            if line == '':
                break
            s = re.search("([a-f0-9]+)\s+(\S+)\s+(\S+)", line)
            if s:
                sym = s.group(3)
                vaddr =  int(s.group(1), 16)
                #print("{} 0x{:x}".format(sym, vaddr))
                if sym == symbol:
                    f_vaddr = vaddr
                    return f_vaddr
                self.symbol[sym] = vaddr
        return f_vaddr

    def get_debug_info(self, addr):
        return "no_vmlinux", 0

    def extract_rtb(self, f, offset, size,  outfile):
        """
        struct msm_rtb_layout {
            unsigned char sentinel[3];
            unsigned char log_type;
            uint32_t idx;
            uint64_t caller;
            uint64_t data;
            uint64_t timestamp;
            uint64_t cycle_count;
        } __attribute__ ((__packed__));
        """
        log_type = [
            'NONE',
            'READL',
            'WRITEL',
            'LOGBUF',
            'HOTPLUG',
            'CTXID',
            'TIMESTAMP',
            'L2CPREAD',
            'L2CPWRITE',
            'IRQ',
        ]

        cpus = 8
        fout = []
        fout_t = []
        mintime = []
        print("Generating msm_rtb<n>.txt...")
        for cpu in range(cpus):
            fout.append(self.open_file("msm_rtb{}.txt".format(cpu), "w"))
            fout_t.append(self.open_file("msm_rtb{}_temp.txt".format(cpu), "w"))
            fout[cpu].write('timestamp, cycle_count, log_type, data, caller, func, line')
            mintime.append(0)
        buf = f.read(size)
        st = "<3sBIQQQQ"
        st_size = struct.calcsize(st)
        off = 0
        cpu = 0
        while off + st_size <= size:
            (sentinel, logtype, idx, caller, data, timestamp, cycle_count) = struct.unpack_from(st, buf, off)
            if sentinel != chr(0xff) + chr(0xaa) + chr(0xff):
                off += st_size
                cpu += 1
                cpu %= cpus
                continue

            if mintime[cpu] == 0:
                mintime[cpu] = timestamp
            fo = fout_t[cpu]
            if timestamp < mintime[cpu]: 
                fo = fout[cpu]
            func, line = self.get_debug_info(caller)
            try:
                log_type_name = log_type[logtype & 0x7f]
            except:
                log_type_name = "(%d)" % logtype


            timestamp = round(float(timestamp)/10**9,6)
            timestamp = format(timestamp,'.6f')

            fo.write('[{0}][0x{1:8x}]:{2:8s} {3:16x} {4:16x} {5} {6}\n'.format(
                timestamp, cycle_count, log_type_name, data, caller, func, line).encode('ascii', 'ignore'))
            off += st_size
            cpu += 1
            cpu %= cpus

        for cpu in range(cpus):
            fout_t[cpu].close()
            fname = "msm_rtb{}_temp.txt".format(cpu)
            self.add_file(fout[cpu], fname, True)
            fout[cpu].close()

    def load_tz_dict(self, dfile):
        for line in open(dfile, "r"):
            try:
                sidline = line.split(':')
                sid = sidline[0]
                self.diag_dict[sid] = []
                self.diag_dict[sid].append(sidline[1])
                self.diag_dict[sid].append(':'.join(sidline[2:]))
            except:
                print "error dict line: %s" % line
                raise

    def translate_tzlog(self, fo, buf):
        for line in buf.split('\n'):
            s = re.search("\[*([0-9a-f]+)\]\s*\(([0-9a-f]+)\s*(.*)\)", line)
            if s:
                sid = s.group(2)
                value = s.group(3).split(' ')
                try:
                    if self.diag_dict.has_key(sid):
                        fm = self.diag_dict[sid][1]
                        if value != ['']:
                            out = fm % tuple(map(lambda x:int(x, 16), value ))
                        else:
                            out = fm
                    else:
                        out = sid + s.group(3)
                    fo.write("[%s] %s %s" % (s.group(1), self.diag_dict[sid][0], out))
                except:
                    if self.diag_dict.has_key(sid):
                        fs = ' '.join(self.diag_dict[sid])
                        fs = fs.strip()
                        fo.write(line.strip() + fs + "\n" )
                    else:
                        fo.write(line)
            else:
                fo.write(line)
                continue

    def extract_tz_bootinfo(self, tz_boot_info, cpu_count):
        """
        struct tzdbg_boot_info_t {
            uint32_t wb_entry_cnt;  /* Warmboot entry CPU Counter */
            uint32_t wb_exit_cnt;   /* Warmboot exit CPU Counter */
            uint32_t pc_entry_cnt;  /* Power Collapse entry CPU Counter */
            uint32_t pc_exit_cnt;   /* Power Collapse exit CPU counter */
            uint32_t warm_jmp_addr; /* Last Warmboot Jump Address */
            uint32_t spare; /* Reserved for future use. */
        };
        /*
         * Boot Info Table for 64-bit
         */
        struct tzdbg_boot_info64_t {
            uint32_t wb_entry_cnt;  /* Warmboot entry CPU Counter */
            uint32_t wb_exit_cnt;   /* Warmboot exit CPU Counter */
            uint32_t pc_entry_cnt;  /* Power Collapse entry CPU Counter */
            uint32_t pc_exit_cnt;   /* Power Collapse exit CPU counter */
            uint32_t psci_entry_cnt;/* PSCI syscall entry CPU Counter */
            uint32_t psci_exit_cnt;   /* PSCI syscall exit CPU Counter */
            uint64_t warm_jmp_addr; /* Last Warmboot Jump Address */
            uint32_t warm_jmp_instr; /* Last Warmboot Jump Address Instruction */
        };
        """
        ptr = 0
        fout = self.open_file("tzcount.txt", "w")
        is_print = False
        online_str = ["ONLINE", "POWER COLLAPSED", "WARM BOOTING" ]
        coreonline = []
        pcsub = []
        wmsub = []
        wbentry = []
        pscisub = []
        if self.hw_id in [ '8940', '8939', '8936', '8937', '8952' ]:
            boot_cpu = 4
        else:
            boot_cpu = 0
        for cpu in xrange(cpu_count):

            st = "<IIII"
            st_size = struct.calcsize(st)
            (wb_entry_cnt, wb_exit_cnt, pc_entry_cnt, pc_exit_cnt) = struct.unpack_from(st, tz_boot_info, ptr)
            wbentry.append(wb_entry_cnt)

            tz64 = True

            (psci_entry_cnt, psci_exit_cnt, warm_jmp_addr32, warm_jmp_instr )  = struct.unpack_from("<IIII", tz_boot_info, ptr + st_size)
            (psci_entry_cnt, psci_exit_cnt, warm_jmp_addr, warm_jmp_instr )  = struct.unpack_from("<IIQI", tz_boot_info, ptr + st_size)

            pcsub.append(0)
            pcsub[cpu] = pc_entry_cnt - pc_exit_cnt
            wmsub.append(0)
            wmsub[cpu] = wb_entry_cnt - wb_exit_cnt

            pscisub.append(0)
            pscisub[cpu] = psci_entry_cnt - psci_exit_cnt

            coreonline.append(0)
            if pcsub[cpu] == wb_entry_cnt - (cpu != boot_cpu): 
                coreonline[cpu] = 0
            else:
                coreonline[cpu] = 1

            if wmsub[cpu] > 0:
                coreonline[cpu] = 2

            if psci_entry_cnt is None: 
                warm_jmp_addr = warm_jmp_addr32
                warm_jmp_instr = 0
                psci_entry_cnt = 0
                psci_exit_cnt = 0
                tz64 = False
                if not is_print:
                    self.print_output(" TZ 32bit")
                    self.print_output("CPU |%-13s|%-13s|%-13s|%-13s|%-21s|%-13s|%-13s|%-13s" % 
                        ("WarmEntry", "WarmExit", "PCEntry", "PCExit", "Warm JumpAddr", "JumpInstr", "PSCIEntry", "PSCIExit"))
                    is_print = True
            else:
                if not is_print:
                    self.print_output(" TZ 64bit")
                    self.print_output("CPU |%-13s|%-13s|%-13s|%-13s|%-21s|%-13s|%-13s|%-13s" % 
                        ("WarmEntry", "WarmExit", "PCEntry", "PCExit", "Warm JumpAddr", "JumpInstr", "PSCIEntry", "PSCIExit"))
                    is_print = True

            ptr += 4*10
            
        #   if tz64:
        #       ptr = ptr + self.ramdump.sizeof("struct tzdbg_boot_info64_t")
        #   else:
        #       ptr = ptr + self.ramdump.sizeof("struct tzdbg_boot_info_t")
            

            self.print_output(" %d  |0x%08x   |0x%08x   |0x%08x   |0x%08x   |0x%016x   |0x%08x  |0x%08x   |0x%08x   " % 
                (cpu, wb_entry_cnt, wb_exit_cnt, pc_entry_cnt, pc_exit_cnt, warm_jmp_addr, warm_jmp_instr, psci_entry_cnt, psci_exit_cnt))

        self.print_output("-----------------------------------------");
        self.print_output("BootCPU: core%d" % boot_cpu)
        for cpu in xrange(cpu_count):
            strs = online_str[coreonline[cpu]]
            self.print_output("CPU core %d is %-20s WarmEntry-WarmExit=0x%08x PCEntry-PCExit=0x%08X|WarmEntry-PC=%02d|PSCI-Exit=0x%08X" %
                (cpu, strs, wmsub[cpu], pcsub[cpu], wbentry[cpu] - pcsub[cpu], pscisub[cpu]))
        fout.close()


    def extract_tz_diagbuf(self, f, offset, size, outfile):
        """
        struct tzdbg_t {
        uint32_t magic_num;
        uint32_t version;
        /*
         * Number of CPU's
         */
        uint32_t cpu_count;
        /*
         * Offset of VMID Table
         */
        uint32_t vmid_info_off;
        /*
         * Offset of Boot Table
         */
        uint32_t boot_info_off;
        /*
         * Offset of Reset info Table
         */
        uint32_t reset_info_off;
        /*
         * Offset of Interrupt info Table
         */
        uint32_t int_info_off;
        /*
         * Ring Buffer Offset
         */
        uint32_t ring_off;
        /*
         * Ring Buffer Length
         */
        uint32_t ring_len;

        /* Offset for Wakeup info */
        uint32_t wakeup_info_off;

        /*
         * VMID to EE Mapping
         */
        struct tzdbg_vmid_t vmid_info[TZBSP_DIAG_NUM_OF_VMID];
        /*
         * Boot Info
         */
        struct tzdbg_boot_info_t  boot_info[TZBSP_MAX_CPU_COUNT];
        /*
         * Reset Info
         */
        struct tzdbg_reset_info_t reset_info[TZBSP_MAX_CPU_COUNT];
        uint32_t num_interrupts;
        struct tzdbg_int_t  int_info[TZBSP_DIAG_INT_NUM];

        /* Wake up info */
        struct tzbsp_diag_wakeup_info_t  wakeup_info[TZBSP_MAX_CPU_COUNT];

        uint8_t key[TZBSP_AES_256_ENCRYPTED_KEY_SIZE];

        uint8_t nonce[TZBSP_NONCE_LEN];

        uint8_t tag[TZBSP_TAG_LEN];

        /*
         * We need at least 2K for the ring buffer
         */
        struct tzdbg_log_t ring_buffer; /* TZ Ring Buffer */
    };

        """

        print("generating {}".format(outfile))
        fo = self.open_file(outfile, "w")
        #diag_buf_off is 0x12000 or  0x13000, so detect
        f.seek(offset)
        off = 0
        while True:
            buf = f.read(8)
            if len(buf) < 8:
                break;
            off += 8
            (magic, version) = struct.unpack_from("<II", buf, 0)
            if magic == 0x747a6461:
                break;
        if magic != 0x747a6461:
            print("Does not found Magic  0x747a6461")
            return

        diag_buf_off = off - 8
        print("Magic:{:x} Version:{:x}".format(magic, version))
        buf = f.read(20)
        (cpu_count, vmid_info_off, boot_info_off, reset_info_off, int_info_off) = struct.unpack_from("<IIIII", buf, 0)
        f.seek(offset + diag_buf_off + boot_info_off)
        buf = f.read(4*10*8)
        self.extract_tz_bootinfo(buf, cpu_count)

        f.seek(offset + diag_buf_off + 28)
        offset += diag_buf_off
        st = "<II"
        st_size = struct.calcsize(st)
        buf = f.read(st_size)
        (ring, ring_len) = struct.unpack_from(st, buf, 0)

        f.seek(offset+ring-2)
        buf = f.read(2)
        (off,) = struct.unpack_from("<H", buf, 0)
        fo.write("Ringstart 0x{:x} , Ring Len: 0x{:x}, Offset:0x{:x}\n".format(ring, ring_len, off))

        f.seek(offset+ring+4)
        str2 = f.read(off - 4)

        f.seek(offset+ring+off)
        str1 = f.read(ring_len - off)

        dict_path =  os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "parsers", "tzlog.dict")
        if not os.path.exists(dict_path):
            dict_path =  os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "tzlog.dict")
        if os.path.exists(dict_path):
            self.load_tz_dict(dict_path)
            self.translate_tzlog(fo, str1+str2)
        else:
            fo.write(str1)
            fo.write(str2)
        fo.write("\n")

    def extract_hyp_diagbuf(self, f, offset, size, outfile):
        """
        struct hypdbg_t {
            /* Magic Number */
            uint32_t magic_num;

            /* Number of CPU's */
            uint32_t cpu_count;

            /* Ring Buffer Offset */
            uint32_t ring_off;

            /* Ring buffer position mgmt */
            struct hypdbg_log_pos_t log_pos;
            uint32_t log_len;

            /* S2 fault numbers */
            uint32_t s2_fault_counter;

            /* Boot Info */
            struct hypdbg_boot_info_t boot_info[TZBSP_MAX_CPU_COUNT];

            /* Ring buffer pointer */
            uint8_t log_buf_p[];
        };

        """
        print("generating {}".format(outfile))
        fo = self.open_file(outfile, "w")
        f.seek(offset)
        head = "<IIIHHII"
        head_size = struct.calcsize(head)

        buf = f.read(head_size)
        (magic, cpu_count, ring_off, wrap, off, log_len, s2_fault_counter) = struct.unpack_from(head, buf, 0)
        print("Magic:{:x} cpu:{:x}".format(magic, cpu_count))
        if magic != 0x6879706d:
            print("Hyp log Magic code not correct")
            return

        fo.write("buffer0x{:x} , len: 0x{:x}, offset:0x{:x}, end:0x{:x}\n".format(ring_off, log_len, off, wrap))

        if off > wrap:
            f.seek(offset+ring_off + wrap)
            strlog = f.read(off - wrap)
        else:
            f.seek(offset+ring_off)
            str2 = f.read(off - 1)
            f.seek(offset + ring_off + wrap)
            str1 = f.read(log_len - wrap)
            strlog = str1 + str2

        fo.write(strlog)
        fo.write("\n")

    def extract_wdog_data(self, f, offset, size, outfile):
        """
        kernel 4.4
    struct msm_watchdog_data {
        unsigned int __iomem phys_base;
        size_t size;
        void __iomem *base;
        void __iomem *wdog_absent_base;
        struct device *dev;
        unsigned int pet_time;
        unsigned int bark_time;
        unsigned int bark_irq;
        unsigned int bite_irq;
        bool do_ipi_ping;
        bool wakeup_irq_enable;
        unsigned long long last_pet;
        unsigned min_slack_ticks;
        unsigned long long min_slack_ns;
        void *scm_regsave;
        cpumask_t alive_mask;
        struct mutex disable_lock;
        bool irq_ppi;
        struct msm_watchdog_data __percpu **wdog_cpu_dd;
        struct notifier_block panic_blk;

        bool enabled;
        bool user_pet_enabled;

        struct task_struct *watchdog_task;
        struct timer_list pet_timer;
        wait_queue_head_t pet_complete;

        bool timer_expired;
        bool user_pet_complete;
        unsigned int scandump_size;
    };
        """

        print("generating {}".format(outfile))
        fo = self.open_file(outfile, "w")
        f.seek(offset+40)
        st = "<IIIIBB6sQ"
        st_size = struct.calcsize(st)
        buf = f.read(st_size)
        (pet_time, bark_time, bark_irq, bite_irq, do_ipi_ping, wakeup_irq_enable, padding, last_pet) = struct.unpack_from(st, buf, 0)
        fo.write("wdog bark_time {} \nwdog pet_time {}\nwdog perform ipi ping {}\nwakeup_irq_enable {}\nlast_pet {}.{:06d}\n".format(bark_time, pet_time, do_ipi_ping, wakeup_irq_enable, last_pet/1000000000, last_pet%1000000000/1000000))
        fo.close()

    def get_strings(self, buf, length):
        offset = 0
        string = ""
        nlist = []
        while offset < length:
            (ch,) = struct.unpack_from("<B", buf, offset)
            offset += 1
            if ch >= 0x30 and ch < 0x80:
                string += chr(ch)
            elif string != "" and len(string) > 3:
                nlist.append(string)
                string = ""
            else:
                string = ""
        return nlist

    def add_file(self, fo, path, delete):
        try:
            fi = self.open_file(path, "rb")   
        except:
            return 
        while True:
            buf = fi.read(4096)
            if len(buf) == 0:
                break
            fo.write(buf)
        fi.close()
        if delete:
            os.unlink(os.path.join(self.out_folder, path))

    def generate_elf(self, outfile, delete=True):
        fo = self.open_file(outfile, "wb")
        print("generating {}".format(outfile))
        fi = self.open_file("md_KELF_HEADER.BIN", "rb")
        buf = fi.read(40000)
        fo.write(buf)
        nlist = self.get_strings(buf, len(buf))
        for names in nlist:
            filepath = "md_" +names+".BIN"
            self.add_file(fo, filepath, delete)
        fi.close()
        fo.close()

    def trans_dmesg(self, rawfile, outfile):
        size = os.path.getsize(rawfile)
        f = self.open_file(rawfile, "rb")
        extract_dmesg(f, 0, size, outfile)
        f.close()

    def extract_dmesg(self, f, offset, size, outfile):
        """
        struct printk_log {
            u64 ts_nsec;        /* timestamp in nanoseconds */
            u16 len;        /* length of entire record */
            u16 text_len;       /* length of text buffer */
            u16 dict_len;       /* length of dictionary buffer */
            u8 facility;        /* syslog facility */
            u8 flags:5;     /* internal record flags */
            u8 level:3;     /* syslog level */
        }
        """
        head = "<QHHHBB"
        head_size = struct.calcsize(head)
        print("generating {}".format(outfile))
        fo = self.open_file(outfile, "w")
        count0 = 0
        f.seek(offset)
        while size > 0:
            rsize = head_size if head_size <= size else size
            read_buff = f.read(rsize)
            read_len = len(read_buff)
            if read_len < head_size:
                size -= read_len
                print("not complete head found {} left:{}".format(read_len, size))
                break
            size -= head_size
            (ts_nsec, lens, text_len, dict_len, facility, flags) = struct.unpack_from(head, read_buff, 0)
            if lens == 0:
                count0 += 1
                continue
            buf = f.read(lens - head_size )
            size -= (lens - head_size)
            dmesg_string = buf[0:text_len]
            fo.write('<{}> [{}.{:06d}] {}\n'.format(flags & 0x07, ts_nsec/1000000000, ts_nsec%1000000000/1000, dmesg_string))

        if count0 > 0:
            print("found len=0 {}".format(count0))
        if size < 0:
            sys.stderr.write("log_buf has corrupt, size({}) < 0".format(size))
        fo.close()

    def extract_general(self, f, offset, size, name):
        fout = self.open_file("reset_status.txt", "a")
        f.seek(offset)
        if name.startswith("md_pmic_pon"):
            rst_stat = f.read(8)
            pmic_pon = struct.unpack_from('BBBBBBBB', rst_stat)
            fout.write("\n")    
            fout.write("PMIC Register (SBL) :\n")   
            fout.write("SBL: PON_REASON_1             : 0x%02x\n" % pmic_pon[0])
            
            fout.write("SBL: WARM_RESET_REASON_1      : 0x%02x\n" % pmic_pon[2])
            fout.write("SBL: WARM_RESET_REASON_2      : 0x%02x\n" % pmic_pon[3])
            
            fout.write("SBL: POFF_REASON_1            : 0x%02x\n" % pmic_pon[4])
            fout.write("SBL: POFF_REASON_2            : 0x%02x\n" % pmic_pon[5])
            fout.write("SBL: PON_SOFT_RESET_REASON_1  : 0x%02x\n" % pmic_pon[6])
            fout.write("SBL: PON_SOFT_RESET_REASON_2  : 0x%02x\n" % pmic_pon[7])
        elif name.startswith("md_rst_stat"):
            rst_stat = f.read(4)
            sbl_gcc_reset_status = struct.unpack_from('I', rst_stat)[0]
            fout.write("SBL: GCC_RESET_STATUS         : 0x%02x\n" % sbl_gcc_reset_status)
        fout.close()
    
    def combined_rawdump(self, in_folder):
        print("combined to sbldump.bin from %s ..." % (in_folder))
        self.out_folder = in_folder
        head = "<8sIIQ8sIQQI";
        head_size = struct.calcsize(head)
        sig = "Raw_Dmp!"
        version = 4096
        valid = 1
        data = 0x200001
        context = "\0\0\0\0\0\0\0\0"
        reset_trigger = 0
        section_count = 0

        section_head = "<IIIQQQQ20s";
        section_head_size = struct.calcsize(section_head)
        
        dump_size =  head_size
        total_size = head_size

        section_type = 3
        valid = 0x1
        info = 0
        temp="sbldump_temp.bin"
        fo = self.open_file(temp, "wb")
        flist = []
        fns = {}
        find_dbg = False
        
        if os.path.exists("dump_info.txt"):
            for line in self.open_file("dump_info.txt", "r"):
                s = re.search("(\S+)\s+([a-fA-F0-9x]+)\s+(\S+)\s+(\S+)", line)
                if s:
                    paddr = int(s.group(2), 16)
                    name = s.group(4)
                    fns[name] = {}
                    fns[name]['paddr'] = paddr
                    fns[name]['exist'] = False

        for line in self.open_file("load.cmm", "r"):
            s = re.search("d.load.binary\s+(\S+)\s+(\S+)", line)
            if s:
                fn = s.group(1)
                if fn == 'md_dbg_table.BIN':
                    find_dbg = True
                ex_list = ['md_KCPU_CTX', 'md_pmic', 'md_KWDOG', 'md_rst_stat', 'md_smem_info', 'md_KMDT0x111']
                paddr = int(s.group(2), 16)
                for ex in ex_list:
                    if fn.startswith(ex):
                        paddr = 0
                flist.append(fn)
                if not fn in fns.keys():
                    fns[fn] = {}
                fns[fn]['paddr'] = paddr
                fns[fn]['exist'] = False

        flist.append('load.cmm')
        flist.append('md_encr_key_aes.BIN')
        flist.append('md_encr_key_iv.BIN')
        flist.append('md_encr_key_mac.BIN')
        if not find_dbg:
            flist.append('md_dbg_table.BIN')

        for item in flist:
            path = os.path.join(in_folder, item)
            if os.path.exists(path):
                section_size = os.path.getsize(path)
                if not item in fns.keys():
                    fns[item] = {}
                    fns[item]['paddr'] = 0
                fns[item]['size'] = section_size
                section_count += 1
                fns[item]['exist'] = True
    
        if 'md_encr_key_aes.BIN' in fns.keys(): 
            padding = 0xc0 - 4
        else:
            padding = 0

        section_offset = head_size + section_head_size * section_count + padding
        dump_size +=  head_size + section_head_size
        total_size = dump_size

        for fn in filter(lambda x:x in fns.keys() and fns[fn]['exist'], flist):
            paddr = fns[fn]['paddr']
            section_size = fns[fn]['size']
            buf = struct.pack(section_head, valid, version, section_type, section_offset, section_size, paddr, info, fn)
            fo.write(buf)
            section_offset += section_size
            dump_size += section_size
            total_size += section_size
        buf = ''
        for i in range(padding):
            buf += '\0'
        fo.write(buf)
        dump_size = (dump_size + 0x100000 -1) & ~0xfffff
        total_size = (total_size + 0x100000 -1) & ~0xfffff
        print "%x" % total_size
        for fn in flist:
            self.add_file(fo, os.path.join(in_folder, fn), False)

        fo.close()

        buf = struct.pack(head, sig, version, valid, data, context, reset_trigger, dump_size, total_size, section_count) 
        fo = self.open_file("sbldump.bin", "wb")
        fo.write(buf)
        self.add_file(fo, temp, True)
        fo.close()


    def split_rawdump(self, rawdump, option='file'):

        head = "<8sIIQ8sIQQI";
        head_size = struct.calcsize(head)

        section_head = "<IIIQQQQ20s";
        section_head_size = struct.calcsize(section_head)
        print("headsize:%d sectionsize:%d" % (head_size, section_head_size))

        filename = os.path.join("", rawdump)
        if not os.path.exists(filename):
            print "rawdump not exist"
            return False
        f = open(filename, "rb")
        head_buf = f.read(head_size)
        (sig, version, valid, data, context, reset_trigger, dump_size, total_size, sections_count) = struct.unpack_from(head, head_buf, 0)
        if sig != "Raw_Dmp!":
            print "rawdump signal is not Raw_Dmp!"
            return False
        if valid != 1:
            print "Valid tag not set!"
            return False
        count = 0
        section_list = []

        while count < sections_count:
            section_buf = f.read(section_head_size)
            section_list.append(section_buf)
            count += 1

        if option == 'list':
            print "File list in rawdump:"
            print("name, section_offset, paddr, section_size, section_type, valid, version")
        elif option == 'split':
            print("Split rawdump %s to seperate file to %s ..." % (rawdump, self.out_folder))

        print("sig:\t%s\nversion:\t%d\nvalid:\t%d\ndata:\t0x%lx\ncontext:\t%s\nreset_trigger:\t%x\ndump_size:\t0x%lx\nTotal Size:\t0x%lx\nSection Count:\t%d\n"
             % (sig, version, valid, data, context, reset_trigger, dump_size, total_size, sections_count))

        if option != 'list':
		    dump_info = self.open_file("dump_info.txt", "w")
		
        for i, one_section in enumerate(section_list):
            valid, version, section_type, section_offset, section_size, paddr, info, name = struct.unpack_from(section_head, one_section, 0)
            name = string.strip(name, '\0')

            if option == 'list':
                print("%s\t0x%x\t0x%x\t0x%x\t%d %d %d " % (name, section_offset, paddr, section_size, section_type, valid, version ))
                continue
            if option == 'kaslr':
                if name.startswith('md_shared_imem'):
                    kaslr_off = self.extract_kaslr_offset(f, section_offset, section_size, '');
                    return kaslr_off
                else:
                    continue
			
            if option != 'list':
                dump_info.write("1 0x%016x\t%16d\t%-16s\t%-16s\n" % (paddr, section_size, name.split('.')[0], name))
            if valid != 1:
                print("%s\t section not valid: 0x%x, size:%d, valid:%d" % (name, paddr, section_size, valid ))
                continue
                
            if name.startswith('md_KMDT0x110'):
                self.extract_dmesg(f, section_offset, section_size, "dmesg.txt");
            if name.startswith('md_KWDOGDATA'):
                self.extract_wdog_data(f, section_offset, section_size, "wdog.txt");
            if name.startswith('md_TZ_IMEM'):
                self.extract_tz_diagbuf(f, section_offset, section_size, "tzlog.txt");
            if name.startswith('md_HYP_DIAG'):
                self.extract_hyp_diagbuf(f, section_offset, section_size, "hyplog.txt");
            if name.startswith('md_pmic_pon') or name.startswith('md_rst_stat'):
                self.extract_general(f, section_offset, section_size, name);
            if name.startswith('md_KRTB'):
                self.extract_rtb(f, section_offset, section_size, "rtb-.txt");
            if name.startswith('md_shared_imem'):
                self.extract_kaslr_offset(f, section_offset, section_size, "loadelf.cmm");

            if option == 'split' or name.startswith('md_K'):
                #print "Writing %s @0x%x len:0x%x ..." % (name, section_offset, section_size),
                fout = self.open_file(name, "wb")
                f.seek(section_offset)
                allread = 0
                block_size = 0x100000 * 10
                left = section_size
                size = block_size if left > block_size else left
                while left > 0:
                    buf = f.read(size)
                    fout.write(buf)
                    allread += size
                    left -= size
                    if allread % (block_size * 20) == 0:
                        print("%d MB ") % (allread / 1024 / 1024)
                    size = block_size if left > block_size else left
                fout.close()
        dump_info.close()
        """
        if option !='list':
            self.generate_elf("ap_minidump.elf", option != 'split')
            try:
                ps = html_result()
                ps.gen_result_html(self.out_folder, self.out_folder)
            except:
                print("Skip to generate html report...")
                pass
        """
        f.close()
        return True

    def __init__(self, out_folder):
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)
        self.out_folder = out_folder

def help():
        print " minidump tool v1.1"
        print "%s [-s|-l|-c|-d|-m|-k] <rawdump> [out_folder] " % sys.argv[0]
        print " -l  list files in sbldump.bin"
        print " -s  split to seperate files"
        print " -c  <folder> combined to sbldump.bin from seperate files in this folder  "
        print " -d  decode dmesg bin file to txt "
        print " -m  check whether vmlinux match by linux banner string"
        print " -k  compare IMEM kaslr offset and calcauted offset from vmlinux linux_banner address"

if __name__=='__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "lsdckm")
    except getopt.GetoptError, err:
        print str(err)
        help()
        sys.exit(-1)

    if len(args) > 0:
        rawdump = args[0]
        if len(args) > 1:
            out_folder = args[1]
        else:
            out_folder = "."
    else:
        help()
        sys.exit(-1)

    mdump = minidump(out_folder)
    option = 'file'
    for opt, val in opts:
        if opt=="-l":
            option = 'list'
            break;
        if opt=="-s":
            option = 'split'
            break;
        if opt=="-d":
            mdump.trans_dmesg(rawdump, "dmesg.txt");
            exit(0);
        if opt=="-c":
            mdump.combined_rawdump(args[0])
            exit(0);
        if opt=="-m":
            mdump.check_banner(rawdump)
            exit(0);
        if opt=="-k":
            imem_off = mdump.split_rawdump(rawdump, 'kaslr')
            off = mdump.get_kaslr_offset()
            print("Calcuate kaslr offset = 0x{:016x}".format(off) ) 
            if imem_off != off:
                print("kaslr offset different, not match vmlinux")
            else:
                print("kaslr offset same, vmlinux could match")
            exit(0);
    mdump.split_rawdump(rawdump, option)
