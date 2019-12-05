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

# install python 3.5.0

```
pyenv install 3.5.0
pyenv global 3.5.0
pip install --upgrade pip
pip install selenium
pip install pandas
```

# use item_page_collector

```
tmux
cd am_scraper
python item_page_collector.py --url
```
