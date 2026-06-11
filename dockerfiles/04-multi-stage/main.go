
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8000"
	}
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello from multi-stage build!")
	})
	fmt.Printf("Listening on :%s\n", port)
	http.ListenAndServe(":"+port, nil)
}
