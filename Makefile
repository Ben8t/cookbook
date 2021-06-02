local:
	@docker pull squidfunk/mkdocs-material && \
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material

run-scraping:
	@python -m cookbook.main
