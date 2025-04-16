IMAGE_NAME=csc488-midterm
PORT=5001

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p $(PORT):5000 $(IMAGE_NAME)

# Optional: run tests inside the container
test:
	docker run --rm $(IMAGE_NAME) pytest --maxfail=1 --disable-warnings -q
