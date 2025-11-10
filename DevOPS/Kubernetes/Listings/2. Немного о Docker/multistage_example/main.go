package main


import (
	"fmt"
	"log"
	"net/http"
)


func handler(w http.ResponseWriter, r *http.Request) {
	//Ответ клиенту
	fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
	
	// Логируем время, путь и статус
	log.Printf("Received request on path %s", r.URL.Path)
}


func main() {
	http.HandleFunc("/", handler)
	log.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}


