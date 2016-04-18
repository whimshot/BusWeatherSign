FROM resin/raspberrypi2-python:latest

# Enable systemd
ENV INITSYSTEM on

# Install Python.
RUN apt-get update && \
    apt-get install -y python python-dev build-essential python-imaging \
    python-pywapi python-pil-doc python-pil-dbg
# Reddmove package lists to free up space
#RUN rm -rf /var/lib/apt/lists/*

# copy current directory into /app
COPY . /app

# run python script when container lands on device
#CMD ["python", "/app/nextbus-matrix.py"]
#CMD ["python", "/app/hello.py"]
#CMD modprobe i2c-dev && python /app/hello.py
#CMD modprobe bcm2708_wdog && python /app/nextbus-matrix.py
CMD ["/bin/bash", "/app/start.sh"]
