## Running the API

\*\*Need to have docker-compse installed in your system.

1. Clone the game-api github respository.

2. In project root, execute following command in a seperate terminal window (ports 5432 and 8000 need to be free before running):
   docker-compose -f docker-compose.local.yml

This will download and build all the docker images. When it is done, you will have the rest api running ad http://localhost:8000.

## Running the tests

```
make run-tests
```
