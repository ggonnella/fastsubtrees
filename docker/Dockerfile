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
RUN apt-get install -y python3.8 python3-pip wget curl git time
RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version=mariadb-10.6
RUN apt-get install -y libmariadb3 libmariadb-dev
RUN pip install mariadb pytest PyYAML sqlalchemy sh pytest-console-scripts
RUN pip install schema snacli
RUN pip install 'ntmirror @ git+https://github.com/ggonnella/fastsubtrees/#subdirectory=ntmirror'
RUN ntmirror-download ntdumpdir
RUN pip install 'fastsubtrees @ git+https://github.com/ggonnella/fastsubtrees'
RUN fastsubtrees-construct ncbi-taxonomy.tree --ntdump ntdumpdir
ARG CACHEBUST=1
RUN git clone -b main https://github.com/ggonnella/fastsubtrees.git /fastsubtrees
COPY ./ntmirror.config.yaml /fastsubtrees/ntmirror/tests/config.yaml
RUN ln -s /ntdumpdir /fastsubtrees/genomes-attributes-viewer/ntdumps
RUN ln -s /ncbi-taxonomy.tree /fastsubtrees/genomes-attributes-viewer/nt.tree
RUN cd /fastsubtrees/genomes-attributes-viewer && pip install -r requirements.txt
RUN cd /fastsubtrees/genomes-attributes-viewer && ./setup.py
EXPOSE 8050
