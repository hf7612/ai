git clone https://github.com/oblique/create_ap
apt-get install hostapd dnsmasq; 
dpkg -i  down/create-ap_189.000f6a2-1_all.deb;
create_ap wlan0 eth0 apname ap_password;    
hostapd /tmp/create_ap.wlan0.conf.ghGF23R2/hostapd.conf;
/usr/sbin/dnsmasq --no-resolv --keep-in-foreground --no-hosts --bind-interfaces --pid-file=/run/sendsigs.omit.d/network-manager.dnsmasq.pid --listen-address=127.0.1.1 --conf-file=/var/run/NetworkManager/dnsmasq.conf --cache-size=0 --proxy-dnssec --enable-dbus=org.freedesktop.NetworkManager.dnsmasq --conf-dir=/etc/NetworkManager/dnsmasq.d;

https://www.ubuntu-tw.org/modules/newbb/viewtopic.php?post_id=349150
