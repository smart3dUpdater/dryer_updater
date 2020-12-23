# dryer
info: 
sudo mkdir /var/www/dryer/public_html
sudo chown -R pi: /var/www/dryer
/var/www/dryer/public_html/

sudo nano /etc/nginx/sites-available/default
sudo systemctl restart nginx

sudo nano /etc/supervisor/supervisord.conf
supervisorctl -c /etc/supervisor/supervisord.conf reload

/etc/X11/xorg.conf.d/99-calibration.conf

poner auto-login con raspi-config
sudo systemctl disable getty@tty1.service

//no sé si sirve este
sudo nano /etc/systemd/system/autologin\@.service
