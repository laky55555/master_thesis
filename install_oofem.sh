#!/bin/bash
apt update

# to download and unzip source (could use git but needs more dependencies)
apt install -y zip wget

# for building and compiling oofem
apt install -y cmake g++

# for using python bindings
# installs boost 1.58 and python2 as dependencies (on ubuntu 16.04)
apt install -y libboost-python-dev

# download and unzip latest oofem source for python2
wget https://github.com/oofem/oofem/archive/5a7fb1b9c723dcca8812ee863a167dede25ec42e.zip
unzip 5a7fb1b9c723dcca8812ee863a167dede25ec42e.zip
mv oofem-5a7fb1b9c723dcca8812ee863a167dede25ec42e/ oofem_src
cd oofem_src

# change cmake file to build oofem with python bindings
sed -i -e '/option.*USE_PYTHON.*OFF/s/OFF/ON/' CMakeLists.txt

mkdir build
cd build
cmake ..
# if cmake couldn't find python interpreter try apt install python2-dev
make

# link shared library so python2 can import it
ln -s "`pwd`/liboofem.so" /usr/local/lib/python2.7/dist-packages/liboofem.so
