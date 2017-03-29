sudo apt-get install python3 python3-pip nginx 

pip3 install --upgrade pip
sudo pip3 install virtualenv

cd /vagrant
# Create a virtual environment
virtualenv word2wizenv
source word2wizenv/bin/activate

# PIP
pip3 install -r requirements.txt

# uwsgi installed from pip
# If uwsgi is installed with apt-get, don't forget to install uwsgi-plugin-python3 too
pip3 install uwsgi

uwsgi -s /tmp/word2wiz.sock --plugin python3 --manage-script-name --mount /=server.app

sudo ln -s /vagrant/config/nginx/sites-available/default /etc/nginx/sites-available/default

sudo ln -s /vagrant/config/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

# sudo ln -s /vagrant/config/uwsgi/init/uwsgi.conf /etc/init/uwsgi.conf

sudo ln -s /vagrant/config/systemd/uwsgi.service /etc/systemd/system/uwsgi.service
