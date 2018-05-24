rm -rf /home/ufo/.UFO/bkp/
rm -rf /home/ufo/.UFO/bkp*.tar.gz
mkdir /home/ufo/.UFO/bkp
mkdir /home/ufo/.UFO/bkp/chipbase
mkdir /home/ufo/.UFO/bkp/xmlbase
mkdir /home/ufo/.UFO/bkp/config
find /home/ufo/.UFO/config/ -type f -size -100 | xargs -n 1 -I % cp  "%"  /home/ufo/.UFO/bkp/config
find /home/ufo/.UFO/chipbase/ -type f -size -10 | xargs -n 1 -I % cp  "%"  /home/ufo/.UFO/bkp/chipbase
find /home/ufo/.UFO/xmlbase/ -type f -size -100M | grep -v xmlchq | xargs -n 1 -I % cp  "%"  /home/ufo/.UFO/bkp/xmlbase
cp /etc/sysconfig/network-scripts/ifcfg* /home/ufo/.UFO/bkp/
tar -zcvf /home/ufo/.UFO/bkp.tar.gz /home/ufo/.UFO/bkp
rm -rf /home/ufo/.UFO/bkp/
