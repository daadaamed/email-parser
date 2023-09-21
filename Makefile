IMAGE_NAME=parser

build:
	@docker build -t $(IMAGE_NAME) .

tests:
ifndef NAME
	@docker run -it -v $(PWD)/src:/usr/src/app -e PYTHONPATH=/usr/src/app $(IMAGE_NAME) pytest -vv
else
	@docker run -it -v $(PWD)/src:/usr/src/app -e PYTHONPATH=/usr/src/app $(IMAGE_NAME) pytest -vv tests/$(NAME).py
endif

clean:
	@docker rmi -f $(IMAGE_NAME)

.PHONY: build tests clean
