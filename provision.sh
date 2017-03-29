sudo apt-get install python3 python3-pip nginx 
pip3 install --upgrade pip

cd /vagrant


sudo pip3 install -r requirements.txt

# uwsgi installed from pip
# If uwsgi is installed with apt-get, don't forget to install uwsgi-plugin-python3 too
pip3 install uwsgi

uwsgi -s /tmp/word2wiz.sock --plugin python3 --manage-script-name --mount /=server.app

sudo ln -s /vagrant/config/nginx/sites-available/default /etc/nginx/sites-available/default
sudo ln -s /vagrant/config/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
sudo ln -s /vagrant/config/uwsgi/init/uwsgi.conf /etc/init/uwsgi.conf
