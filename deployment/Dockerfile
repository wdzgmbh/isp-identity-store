FROM debian:12

RUN apt-get update && apt-get install -y freeradius freeradius-rest

RUN rm /etc/freeradius/3.0/sites-available/*
RUN rm /etc/freeradius/3.0/sites-enabled/*
RUN rm /etc/freeradius/3.0/mods-enabled/eap

COPY freeradius /etc/freeradius/3.0

RUN cd /etc/freeradius/3.0/mods-enabled && ln -s ../mods-available/rest
RUN cd /etc/freeradius/3.0/sites-enabled && ln -s ../sites-available/rest

CMD ["freeradius", "-X"]