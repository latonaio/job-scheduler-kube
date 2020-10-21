FROM l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=job-scheduler \
    AION_HOME=/var/lib/aion \
    MYSQL_SERVICE_HOST=mysql \
    MYSQL_USER=latona \
    MYSQL_PASSWORD=latonalatona

RUN mkdir ${AION_HOME}
WORKDIR ${AION_HOME}

# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/
ADD . .

#RUN apt-get update && apt-get install -y libyaml-dev
#RUN pip3 install -U setuptools
#RUN rm -rf /usr/local/lib/python3.6/dist-packages/protobuf*

RUN pip3 install -U requests pyyaml
RUN rm -rf /usr/local/lib/python3.6/dist-packages/protobuf*
RUN pip3 install -U kubernetes protobuf docker
RUN python3 setup.py install

CMD ["/bin/sh", "docker-entrypoint.sh"]
