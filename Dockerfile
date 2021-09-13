FROM python:3.7

ARG PYTHON_INTERPRETER
ARG PORT

ENV PYTHON_INTERPRETER=$PYTHON_INTERPRETER
ENV PORT=$PORT

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
CMD $PYTHON_INTERPRETER -m bokeh serve app --show --port=$PORT
