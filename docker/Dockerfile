# syntax=docker/dockerfile:1
FROM mariadb:10.6
ARG MARIADB_ROOT_PASSWORD=rootpass
ENV MARIADB_ROOT_PASSWORD=$MARIADB_ROOT_PASSWORD
USER root
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.8 python3-pip wget curl git
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version=mariadb-10.6
RUN apt-get install -y libmariadb3 libmariadb-dev
RUN git clone https://github.com/ggonnella/fastsubtrees
RUN pip install mariadb pytest PyYAML sqlalchemy
