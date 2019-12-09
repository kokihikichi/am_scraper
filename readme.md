# download commands

```
sudo yum -y install gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git tmux wget unzip libX11
```

# git clone

```
git clone https://github.com/kokihikichi/am_scraper.git
```

# chrome & chrome driver

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum -y install ./google-chrome-stable_current_*.rpm
wget https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
cp chromedriver ./am_scraper/
```

# pyenv

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

# python install

```

wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar xzf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make altinstall
sudo /usr/local/bin/pip3.5 install --upgrade pip
sudo /usr/local/bin/pip3.5 install selenium
sudo /usr/local/bin/pip3.5 install pandas
```

# use item_page_collector

```
tmux
cd am_scraper
python item_page_collector.py --url
```

# remove & create vm instances

```
gcloud compute instances -q delete "am-scraper-1" --zone=us-central1-a

gcloud compute --project "window-shopping-app" disks create "am-scraper-1" --size "10" --zone "us-central1-a" --source-snapshot "am-scraper-snapshot-1" --type "pd-standard"

gcloud beta compute --project=window-shopping-app instances create am-scraper-1 --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=9654041822-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --disk=name=am-scraper-1,device-name=am-scraper-1,mode=rw,boot=yes,auto-delete=yes --reservation-affinity=any
```

# set systemd

```
sudo cp ./start_scrape_2.sh /usr/bin/start_scrape_2.sh
sudo chmod +x /usr/bin/start_scrape_2.sh
sudo cp myservice.service /etc/systemd/system/myservice.service
sudo chmod 644 /etc/systemd/system/myservice.service
```

# sudo vi /usr/bin/start_scrape_2.sh

```
cd /home/koki_hikichi/am_scraper
/usr/bin/python3.5 /home/koki_hikichi/am_scraper/item_page_scraper.py --update_flg alt_images
```

# startup_script

```
gsutil cp gs://am-scraped/startup_scripts/am-scraper-6.sh /home/koki_hikichi/am_scraper/
sudo chmod +x /home/koki_hikichi/am_scraper/am-scraper-6.sh
/home/koki_hikichi/am_scraper/am-scraper-6.sh
```

# am-scraper-X.sh

```
cd /home/koki_hikichi/am_scraper
rm df_main.pickle item_links.pickle current_url.pickle
gsutil cp gs://am-scraped/bk/am-scraper-6-df_main.pickle /home/koki_hikichi/am_scraper/df_main.pickle
gsutil cp gs://am-scraped/bk/am-scraper-6-item_links.pickle /home/koki_hikichi/am_scraper/item_links.pickle
gsutil cp gs://am-scraped/bk/am-scraper-6-current_url.pickle /home/koki_hikichi/am_scraper/current_url.pickle
git pull --rebase
python item_page_scraper.py 6 --update_flg alt_images

```
