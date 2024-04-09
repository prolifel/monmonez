run:
	granian --interface asgi main:app --port 8000 --log

save-pip:
	pip freeze > requirements.txt