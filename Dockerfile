FROM resin/raspberrypi-python

# Enable systemd
ENV INITSYSTEM on

# Install Python.
RUN apt-get update \
	&& apt-get install -y apt-utils \
    && apt-get install -y python python-dev python-imaging python-pywapi \
	# Remove package lists to free up space
	&& rm -rf /var/lib/apt/lists/*

# copy current directory into /app
COPY . /app

# run python script when container lands on device
#CMD ["python", "/app/nextbus-matrix.py"]
CMD modprobe i2c-dev && python /app/nextbus-matrix.py
