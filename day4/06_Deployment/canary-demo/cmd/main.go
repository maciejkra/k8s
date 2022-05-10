package main

import (
	"encoding/json"
	"github.com/sirupsen/logrus"
	"net/http"
	"os"
	"sync"
)

type resp struct {
	Resp int `json:"calls"`
}

type vers struct {
	V string `json:"version"`
}

var (
	requests int = 0
	protect  sync.Mutex
)

func increment() {
	protect.Lock()
	defer protect.Unlock()
	requests++
}

func call() int {
	protect.Lock()
	defer protect.Unlock()
	return requests
}

func returnMetrics(rw http.ResponseWriter, req *http.Request) {
	rw.WriteHeader(http.StatusOK)
	data, err := json.Marshal(resp{Resp: call()})
	if err != nil {
		logrus.Errorln(err)
	}
	rw.Write(data)
}

func reset(rw http.ResponseWriter, req *http.Request) {
	protect.Lock()
	defer protect.Unlock()
	requests = 0
	rw.WriteHeader(http.StatusOK)
}

func returnVersion(v string) func(http.ResponseWriter, *http.Request) {
	return func(rw http.ResponseWriter, req *http.Request) {
		increment()
		rw.WriteHeader(http.StatusOK)
		data, err := json.Marshal(vers{V: v})
		if err != nil {
			logrus.Errorln(err)
		}
		rw.Write(data)
	}
}

func env() string {
	return os.Getenv("VERSION")
}

func main() {
	version := env()
	http.HandleFunc("/version", returnVersion(version))
	http.HandleFunc("/metrics", returnMetrics)
	http.HandleFunc("/reset", reset)
	logrus.Infoln("HTTP Server is up and listening ...")
	logrus.Fatalln(http.ListenAndServe(":8080", nil))
}
