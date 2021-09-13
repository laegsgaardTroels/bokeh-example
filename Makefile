PYTHON_INTERPRETER := python3
DEV_PORT := 8080
PROD_PORT := 8080
CONTAINER_NAME := real-estate-bokeh-example-container
IMAGE_TAG := real-estate-bokeh-example-image

.PHONY: dev
dev: .venv/bin/activate
	. .venv/bin/activate; \
		${PYTHON_INTERPRETER} -m bokeh serve app --show --port=${DEV_PORT}

.PHONY: docker
docker: docker_build docker_run

.PHONY: docker_run
docker_run:
	docker rm -f ${CONTAINER_NAME} || true
	docker run \
		-d \
		-p ${PROD_PORT}:${PROD_PORT} \
		--name ${CONTAINER_NAME} \
		${IMAGE_TAG}

.PHONY: docker_build
docker_build:
	docker build \
		-t ${IMAGE_TAG} \
		--no-cache \
		--build-arg PYTHON_INTERPRETER=${PYTHON_INTERPRETER} \
		--build-arg PORT=${PROD_PORT} \
		.

.venv/bin/activate: requirements.txt
	rm -rf .venv
	${PYTHON_INTERPRETER} -m pip install --upgrade pip
	${PYTHON_INTERPRETER} -m pip install --upgrade setuptools
	${PYTHON_INTERPRETER} -m pip install --upgrade virtualenv
	virtualenv --python ${PYTHON_INTERPRETER} .venv
	. .venv/bin/activate; \
		${PYTHON_INTERPRETER} -m pip install -r requirements.txt;
