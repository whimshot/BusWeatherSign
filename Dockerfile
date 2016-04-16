FROM resin/raspberrypi-python

# Enable systemd
ENV INITSYSTEM on

# Install Python.
RUN apt-get update

RUN apt-get install -y apt-utils

RUN apt-get install -y python python-dev

# Remove package lists to free up space
RUN rm -rf /var/lib/apt/lists/*

# copy current directory into /app
COPY . /app

# run python script when container lands on device
#CMD ["python", "/app/nextbus-matrix.py"]
CMD modprobe i2c-dev && apt-get update && apt-get install -y python-imaging python-pywapi && python /app/nextbus-matrix.py
