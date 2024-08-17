This is how to set it up

Update and install dependencies:
'''
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev

'''

Download Python 3.8 source code:
'''
curl -O https://www.python.org/ftp/python/3.8.16/Python-3.8.16.tgz
tar -xf Python-3.8.16.tgz
cd Python-3.8.16

'''


Configure and build Python:
'''
./configure --enable-optimizations --prefix=$HOME/python3.8
make -j$(nproc)
make install

'''

Add Python 3.8 to your PATH (temporarily or permanently):
'''
export PATH=$HOME/python3.8/bin:$PATH
'''

Create a virtual environment using Python 3.8:
'''
python3.8 -m venv myenv
'''

Activate the virtual environment:
'''

source myenv/bin/activate
'''







