FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 53
RUN apt-get update && apt-get install -y supervisor
COPY dnsOverTls.py /
COPY App.py /
COPY ca-certificate.crt /
COPY logger.py /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/log/dns-over-tls/
CMD ["/usr/bin/supervisord"]
