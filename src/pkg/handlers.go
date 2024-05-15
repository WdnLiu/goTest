package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

type Instrument struct {
	Name      string `json:"name"`
	Intervals []bool `json:"intervals"`
}

type CarnaticData struct {
	Instruments []Instrument `json:"instruments"`
}

func GenerateAndWriteJSON(fileName string) error {
	// Seed the random number generator
	rand.NewSource(time.Now().UnixNano())

	// Helper function to generate random boolean intervals
	generateRandomIntervals := func(length int) []bool {
		intervals := make([]bool, length)
		for i := range intervals {
			intervals[i] = rand.Intn(2) == 1
		}
		return intervals
	}

	// Define the directory for storing data files
	directory := "data"

	// Ensure the directory exists
	if err := os.MkdirAll(directory, 0755); err != nil {
		return fmt.Errorf("error creating directory: %v", err)
	}

	// Define the file path for the JSON file
	filePath := filepath.Join(directory, fileName)

	// Create the output file in the specified directory
	file, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("error creating file: %v", err)
	}
	defer file.Close()

	// Define the Carnatic instruments with random boolean intervals
	data := CarnaticData{
		Instruments: []Instrument{
			{
				Name:      "Veena",
				Intervals: generateRandomIntervals(10),
			},
			{
				Name:      "Mridangam",
				Intervals: generateRandomIntervals(10),
			},
			{
				Name:      "Flute",
				Intervals: generateRandomIntervals(10),
			},
			{
				Name:      "Violin",
				Intervals: generateRandomIntervals(10),
			},
			{
				Name:      "Kanjira",
				Intervals: generateRandomIntervals(10),
			},
			{
				Name:      "Ghatam",
				Intervals: generateRandomIntervals(10),
			},
		},
	}

	// Convert the data to JSON
	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return fmt.Errorf("error marshalling to JSON: %v", err)
	}

	// Write the JSON data to the file
	_, err = file.Write(jsonData)
	if err != nil {
		return fmt.Errorf("error writing to file: %v", err)
	}

	return nil
}

func HandleGenerateJSON(w http.ResponseWriter, r *http.Request) {
	fileName := "input.json"
	err := GenerateAndWriteJSON(fileName)
	if err != nil {
		http.Error(w, "Error generating JSON: "+err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("JSON file successfully created"))
}

func IndexHandler(w http.ResponseWriter, r *http.Request) {
	// Serve the HTML file
	http.ServeFile(w, r, "src/html/index.html")
}
