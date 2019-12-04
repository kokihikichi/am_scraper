# download commands

sudo yum -y install gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git tmux wget unzip libX11

# git clone

git clone https://github.com/kokihikichi/am_scraper.git

# chrome driver

wget https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
cp chromedriver ./am_scraper/

# pyenv

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "\$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile

# install python 3.5.0

pyenv install 3.5.0
pyenv global 3.5.0
pip install --upgrade pip
pip install selenium
pip install pandas