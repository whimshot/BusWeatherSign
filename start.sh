# load watchdog kernal module
modprobe bcm2708_wdog && echo "Hardware Watchdog Enabled"

if [ -e "/dev/watchdog" ]
then
    echo "Found /dev/watchdog"
fi
# Run your application here
/usr/bin/python /app/nextbus-matrix.py

# unmount hardware watchdog when the container is killed
trap 'modprobe -r bcm2708_wdog' SIGTERM
# wait indefinitely
while :
do
	sleep 1
done
