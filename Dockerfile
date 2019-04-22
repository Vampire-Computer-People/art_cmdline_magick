FROM python:3.7-alpine

COPY ./ ./art_command_line_imagemagick

ENV MAGICK_HOME=/usr

RUN apk --update add imagemagick && \
	apk --update add imagemagick-dev && \
    rm -rf /var/cache/apk/* && \
	pip install -r art_command_line_imagemagick/requirements.txt
