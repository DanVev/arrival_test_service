FROM golang:latest
RUN mkdir /app
ADD . /app/
WORKDIR /app
ENV GO111MODULE=auto
RUN go get "github.com/gorilla/websocket"
RUN go get "github.com/icrowley/fake"
RUN go build -o main .
EXPOSE 8080
CMD ["/app/main"]