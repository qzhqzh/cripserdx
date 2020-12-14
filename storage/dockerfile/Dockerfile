From ubuntu:18.04

MAINTAINER 28630707@qq.com
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    apache2 \
    libapache2-mod-wsgi-py3 \
    libcurl4-openssl-dev \
    libssl-dev \
    supervisor \
    curl \
    cpio \
    clinfo

# development tools, could be remove in product
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs \
    vim \
    wget \
    ipython \
    net-tools \
    inetutils-ping \
    lsof \
    less \
    git

COPY install_required/ /tmp/install_required/

RUN python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 --default-timeout=1000 install -r /tmp/install_required/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# crispr-offinder requirements
# note: 1.remove python2 link 2.biopython==1.60
RUN rm /usr/local/bin/pip
RUN cd /tmp/install_required/ && tar -xvf  /tmp/install_required/l_opencl_p_18.1.0.015.tgz
RUN cd /tmp/install_required/l_opencl_p_18.1.0.015 && sh install.sh

RUN /bin/bash /tmp/install_required/gen_apache2_conf.sh /home/site/html/dist /home/site/api/storage/logs/apache2 /home/site/api > /etc/apache2/sites-available/crisperdx.conf \
    && sed -i 's:export lang=c:export lang=c.utf-8:g' /etc/apache2/envvars \
    && echo "listen 9003" >> /etc/apache2/ports.conf \
    && echo "listen 9004" >> /etc/apache2/ports.conf \
    && a2enmod rewrite

RUN ln -s /etc/apache2/sites-available/crisperdx.conf /etc/apache2/sites-enabled/crisperdx.conf
#RUN mv /tmp/install_required/supervisor-crisperdx.conf /etc/supervisor/conf.d/

RUN rm -rf /tmp/install_required/
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]