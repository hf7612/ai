# grep -e 'logcat -b events' -A 10000000 $1 |grep -B 10000000 'was the duration of .*EVENT LOG' > $2;c $2

# ------ SYSTEM LOG (logcat -v threadtime -v printable -v uid -d *:v) ------
# was the duration of 'SYSTEM LOG' ------
# ------ EVENT LOG (logcat -b events -v threadtime -v printable -v uid -d *:v) ------
# was the duration of 'EVENT LOG' ------
# ------ RADIO LOG (logcat -b radio -v threadtime -v printable -v uid -d *:v) ------
# was the duration of 'RADIO LOG' ------
set -x
grep ' SYSTEM LOG .*logcat .* threadtime ' -A 10000000000 $1 |grep -B 10000000000 "was the duration of .RADIO LOG" > /tmp/logcat_all.log;
grep -B 10000000000 'was the duration of .SYSTEM LOG' /tmp/logcat_all.log > logcat_tmp.log;
grep -A 10000000000 ' EVENT LOG .logcat' /tmp/logcat_all.log|grep -B 10000000000 'was the duration of .EVENT LOG'  > event_tmp.log;
grep -A 10000000000 'RADIO LOG .logcat' /tmp/logcat_all.log > radio_tmp.log;
