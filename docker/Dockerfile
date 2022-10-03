# syntax=docker/dockerfile:1
FROM mariadb:10.6
ARG MARIADB_ROOT_PASSWORD=rootpass
ARG MARIADB_PASSWORD=mypass
ARG MARIADB_USER=myuser
ENV MARIADB_ROOT_PASSWORD=$MARIADB_ROOT_PASSWORD
ENV MARIADB_PASSWORD=$MARIADB_PASSWORD
ENV MARIADB_USER=$MARIADB_USER
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
RUN pip install mariadb pytest PyYAML sqlalchemy sh pytest-console-scripts
RUN git clone https://github.com/ggonnella/fastsubtrees
RUN cd fastsubtrees/ntmirror && pip install -e .
RUN cd fastsubtrees && pip install -e .
COPY ./ntmirror.config.yaml /fastsubtrees/ntmirror/tests/config.yaml
COPY ./create_db.sql /fastsubtrees/ntmirror/tests/create_db.sql
#RUN mysqld_safe --user=root --password=$MARIADB_ROOT_PASSWORD \
#                --datadir=/var/lib/mysql/ \
#                --log-error=/var/log/mysql/error.log \
#                --pid-file=/run/mysqld/mysqld.pid \
#                --socket=/run/mysqld/mysqld.sock \
#                --port=3306 &
#RUN sleep 3
#RUN mariadb --socket=/run/mysqld/mysqld.sock \
#            -u root -p$MARIADB_ROOT_PASSWORD < /fastsubtrees/ntmirror/tests/create_db.sql
