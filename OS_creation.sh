#!/bin/bash
echo "Updating system..."
apt update
apt upgrade

#instala GIT
apt -y install git

#install ngnix
apt install nginx -y
sudo /etc/init.d/nginx start

apt install supervisor -y

#Instala tool para calibrar touch resistivo
apt -y install xinput-calibrator
apt -y install xserver-xorg-input-evdev
cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf

#echo "deb https://packages.erlang-solutions.com/debian stretch contrib" | sudo tee /etc/apt/sources.list.d/erlang-solutions.list
wget https://packages.erlang-solutions.com/debian/erlang_solutions.asc
sudo apt-key add erlang_solutions.asc
sudo apt update
sudo apt -y install elixir
echo "export PATH=/home/pi/miniconda3/bin:\$PATH" >> /etc/bash.bashrc
(
    cd /home/pi
    wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
    bash Miniconda3-latest-Linux-armv7l.sh -p /home/pi/miniconda3 -b
    rm -fr Miniconda3-latest-Linux-armv7l.sh
)
#instalacion de conda y un python mas moderno
(
cd /home/pi/miniconda3/bin
./conda config --add channels rpi
./conda install python=3.6 -y
)

apt remove -y --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm
apt install -y busybox-syslogd ntp chromium-browser xorg unclutter
dpkg --purge rsyslog

#Ver lo de pip, deberia estar instalado
chown -R pi:pi /home/pi

cat <<EOF > /usr/bin/start-chromium
#!/bin/bash -e
#xscreensaver -no-splash
xset s off
xset -dpms
xset s noblank
unclutter &
while [ 1 ] ; do
	sudo -u pi chromium-browser "\$@" \
			--window-size=800,480 \
			--incognito \
			--disable-pinch \
			--overscroll-history-navigation=0 \
			--kiosk \
			--window-position=0,0 \
			--start-fullscreen \
			http://localhost:8888/home
#			--noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI --disk-cache-dir=/dev/null 
done
EOF

cat <<EOF > /usr/bin/stop-chromium
#!/bin/bash -e
pkill -TERM start-chromium
EOF

cat <<EOF > /etc/X11/xorg.conf
Section "ServerFlags"
    Option "DontVTSwitch" "true"
EndSection
EOF

chmod a+x /usr/bin/start-chromium