# Arrival Vehicle reader
Websocket-based service built on AIOHTTP written for Arrival Ltd.

## Repository structure
* vehicle_emulator - a websocket with constantly-generated data about vehicles with the following format:
  ```
  {
  "component": "Realbridge Air Amplifier",
  "country": "Argentina",
  "description": "ut rerum ut quis nulla quasi quis est autem.",
  "model": "mh 80151"
  }
  ```
  More techincal details can be found in  `vehicle_emulator/README.md`
* websocket_reader - an asynchronous service which reads data from websocket and writes them to MongoDB. It can retrieve saved data via http GET request, e.g. 
  ```
  http://localhost:1234
  ```
  or 
  ```
  http://localhost:1234?page=N
  ```
to get N page of database (page size is set to 50)

## Run services
  Prerequisites: docker, docker-compose
  1. Clone a repo, cd to a top-level folder
  2. Execute 
  ```
  docker-compose up --build
  ```
  to run the services. Data can be accessed via `http://localhost:1234`, you should see something like:
  ![image](https://user-images.githubusercontent.com/19992467/125583951-fdcee901-f0f5-4f5f-9e30-5f390e304f69.png)
  3. Execute
  ```
  docker-compose down
  ```
  to stop all running service containers
