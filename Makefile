
techsync:
	cd ../; rsync -av --exclude=.git tech_sky130B/ tech_sky130A
	egrep -R "sky130B"|awk -F: '{print $1}'|sort|uniq|egrep -v "^\.git" > sky130B.txt
