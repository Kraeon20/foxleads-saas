// Add this code to your JavaScript file, e.g., apiconnect.js

// Get drop zone element
const dropZone = document.getElementById("drop-zone");

// Add event listeners for drag and drop
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(event) {
  event.preventDefault();
  event.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight() {
  dropZone.classList.add("highlight");
}

function unhighlight() {
  dropZone.classList.remove("highlight");
}

// Handle drop event
dropZone.addEventListener("drop", handleDrop, false);

function handleDrop(event) {
  const files = event.dataTransfer.files;
  handleFiles(files);
}

// Handle file selection from file input
document
  .getElementById("file-input")
  .addEventListener("change", handleFileInput);

function handleFileInput(event) {
  const files = event.target.files;
  handleFiles(files);
}

// Function to handle dropped or selected files
function handleFiles(files) {
  for (const file of files) {
    // Check if it's a valid file
    if (isValidFile(file)) {
      // Read the contents of the file
      const reader = new FileReader();

      reader.onload = function (e) {
        const contents = e.target.result;
        // Parse the contents to extract numbers
        const numbers = parseFileContents(contents);
        // Display numbers or further process them
        displayUploadedNumbers(numbers);
      };

      reader.readAsText(file);
    } else {
      // Handle invalid file type
      console.error("Invalid file type");
    }
  }
}

// Function to check if file type is valid
function isValidFile(file) {
  const validTypes = ["text/plain", "text/csv"];
  return validTypes.includes(file.type);
}

// Function to parse file contents and extract numbers
function parseFileContents(contents) {
  // Here you need to implement logic to parse the file contents and extract numbers
  // Example: You might split the contents by newline character and extract numbers from each line
  // Implement your parsing logic here
}

// Function to display uploaded numbers
function displayUploadedNumbers(numbers) {
  // Here you can display the numbers in the UI or further process them as needed
  const numbersContainer = document.getElementById("generated-numbers");
  // Clear previous content
  numbersContainer.innerHTML = "";
  // Append each number to the container
  numbers.forEach((number) => {
    const numberElement = document.createElement("div");
    numberElement.textContent = number;
    numbersContainer.appendChild(numberElement);
  });
}
