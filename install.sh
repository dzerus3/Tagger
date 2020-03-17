#!/bin/sh
# Author: Dellon Zerus
# A.K.A. A. Sushko

RED='\033[0;31m' 
PURPLE='\033[0;35m'
NC='\033[0m'

# Check for python and pip, then install
function check_deps {
	if command -v pip3 > /dev/null && command -v python3 > /dev/null; then
        echo "Installing module dependencies..."
		pip3 install requests bs4 argparse > /dev/null
	else
        echo "It appears you're missing either ${RED}python3${NC} or ${RED}pip3${NC}... Install those first."
		exit 1
	fi
}

#check if run as root
if [[ "$(id -u)" -ne 0 ]]; then
   printf "\e[1;77mThis won't work without root. Try ${PURPLE}sudo ./install.sh${NC}\n\e[0m"
   exit 1
fi

check_deps

echo "Moving the ${RED}executable...${NC}"
cp tagger.py /usr/bin/tagger
echo "Creating ${RED}manpage...${NC}"
gzip -k tagger.1
cp tagger.1.gz /usr/share/man/man1/tagger.1.gz
echo "We're done here. Try running ${PURPLE}tagger --help${NC}"
