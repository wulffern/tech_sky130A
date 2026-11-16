#!/usr/bin/env bash
#- Install the TinyTapeout top level and default block into a new IP.
#
# Usage (run from the IP root, after the tech symlink exists):
#   bash tech/cicconf/rey_tt.sh <IP> <CELL> <cell>
#   e.g. bash tech/cicconf/rey_tt.sh REY_GR01_SKY130A REY_GR01 rey_gr01
#
# Copies every file in tech/cicconf/rey_tt/ to design/<IP>/, replacing
# @IP@, @CELL@ and @cell@ in both file names and contents.
set -euo pipefail

if [ $# -ne 3 ]; then
    echo "Usage: $0 <IP> <CELL> <cell>" >&2
    exit 1
fi

IP=$1
CELL=$2
cell=$3
SRC=$(dirname "$0")/rey_tt
DST=design/$IP

mkdir -p "$DST"
for f in "$SRC"/*; do
    n=$(basename "$f")
    n=${n//@IP@/$IP}
    n=${n//@CELL@/$CELL}
    n=${n//@cell@/$cell}
    IP=$IP CELL=$CELL cell=$cell perl -pe 's/\@IP\@/$ENV{IP}/g; s/\@CELL\@/$ENV{CELL}/g; s/\@cell\@/$ENV{cell}/g' "$f" > "$DST/$n"
    echo "rey_tt: $DST/$n"
done
