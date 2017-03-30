#!/usr/bin/env bash

apt-get update
apt-get install -y python3 python3-pip nginx default-jre

pip3 install --upgrade pip
pip3 install virtualenv

# The sources should be stored in /var/www/word2wiz. Otherwise, try to link them from vagrant folder
wwwroot=/var/www/word2wiz

# If using vagrant, link the folder
if [ -d /vagrant ]; then
    if ! [ -L $wwwroot ]; then
        rm -rf $wwwroot
        ln -fs /vagrant $wwwroot
    fi
elif ! [ -d $www-root ]; then
    echo "ERROR: $wwwroot does not exist"
    exit -1
fi

cd $wwwroot

# Create a virtual environment
virtualenv word2wizenv
source word2wizenv/bin/activate

# PIP
pip3 install -r requirements.txt

# Extra packages in the virtual environment:
# If uwsgi is installed with apt-get, don't forget to install uwsgi-plugin-python3 too
pip3 install uwsgi

rm -f /etc/nginx/sites-available/default
ln -s $wwwroot/config/nginx/sites-available/default /etc/nginx/sites-available/default

# ln -s $wwwroot/config/uwsgi/init/uwsgi.conf /etc/init/uwsgi.conf

# Links cause problems in systemd. So copy instead
#ln -s $wwwroot/config/systemd/uwsgi.service /etc/systemd/system/uwsgi.service
rm -f /etc/systemd/system/uwsgi.service
cp $wwwroot/config/uwsgi/systemd/uwsgi.service /etc/systemd/system/uwsgi.service

# When using vagrant, the services shuould wait until the sync directory is mounted:
sed -i 's/WantedBy=multi-user.target/WantedBy=vagrant.mount/' /etc/systemd/system/uwsgi.service

#########
# SPELL #
#########

SPELL_VERSION=v0.2-alfa
SPELL_PKG_NAME=spell-$SPELL_VERSION.tar
SPELL_URL=https://github.com/joserc87/spell/releases/download/$SPELL_VERSION/$SPELL_PKG_NAME.tar

# Instal spell (if not installed)
if ! hash "spell" 2>/dev/null; then
    cd /tmp
    wget $SPELL_URL
    tar -xvf $SPELL_PKG_NAME.tar
    mv -R $SPELL_PKG_NAME /usr/local/bin
    ln -s /usr/local/bin/$SPELL_PKG_NAME/bin/spell /usr/local/bin/spell
    rm $SPELL_PKG_NAME.tar
fi

# Reload systemd services
systemctl daemon-reload

systemctl reload nginx
systemctl stop uwsgi
systemctl start uwsgi

systemctl disable uwsgi.service
systemctl enable uwsgi.service
systemctl disable nginx.service
systemctl enable nginx.service
