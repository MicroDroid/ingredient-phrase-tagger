FROM mtlynch/crfpp
LABEL maintainer="Yousef Sultan <mail@overcoder.dev>"

ARG BUILD_DATE
ENV VCS_URL https://github.com/MicroDroid/ingredient-phrase-tagger.git
ARG VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
	org.label-schema.vcs-url="$VCS_URL" \
	org.label-schema.vcs-ref=$VCS_REF \
	org.label-schema.schema-version="1.0.0-rc1"

RUN apt-get update -y && \
	apt-get install -y git python3 python3-pip

WORKDIR /app
COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

RUN rm -rf /var/lib/apt/lists/* && \
	rm -Rf /usr/share/doc && \
	rm -Rf /usr/share/man && \
	apt-get autoremove -y && \
	apt-get clean

COPY . .

ENV PYTHONPATH=/app/ \
	LABELLED_DATA_FILE=nyt-ingredients-snapshot-2015.csv \
	LABELLED_EXAMPLE_COUNT=0 \
	TRAINING_DATA_PERCENT=0.1 \
	CRF_TRAINING_THREADS=8 \
	OUTPUT_DIR=./models

RUN ./bin/train-model ./models

ENTRYPOINT [ "uwsgi", "--threads", "4", "--http-socket", ":8080", "--wsgi-file", "server.py" ]

EXPOSE 8080
