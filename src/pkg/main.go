package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/generate-json", HandleGenerateJSON)
	http.HandleFunc("/", IndexHandler)

	fmt.Println("Server started at :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
