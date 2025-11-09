FROM python:3.10-alpine
RUN apk add --no-cache --update socat

WORKDIR /chal
COPY experiments/exp_padding_oracle/requirements.txt /chal/
COPY experiments/exp_padding_oracle/vuln.py /chal/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["socat", "-t", "900", "-T", "120", "TCP4-LISTEN:1337,reuseaddr,fork", "EXEC:env PYTHONUNBUFFERED=1 python3 /chal/vuln.py"]