document.addEventListener("DOMContentLoaded", function () {
  const stateSelect = document.getElementById("state-select");
  const citySelect = document.getElementById("city-select");
  const areaCodeSelect = document.getElementById("area-code-select");

  // Add event listener to the "Validate File" button
  const validateFileBtn = document.getElementById("validate-file-btn");
  validateFileBtn.addEventListener("click", validateFile);

  async function validateFile() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
      // Display an error message if no file is selected
      document.getElementById("error-message").textContent =
        "Please select a file.";
      return;
    }

    // Clear any previous error messages
    document.getElementById("error-message").textContent = "";

    try {
      // Read the file content as text
      const fileText = await file.text();

      // Split the text content by newline character to get each line
      const lines = fileText.split("\n");

      // Extract numbers from the file lines and send them for validation
      for (const line of lines) {
        const numbers = line.trim().split(","); // Assuming numbers are comma-separated
        for (const number of numbers) {
          await validateNumber(number);
        }
      }
    } catch (error) {
      console.error("Error reading file:", error);
      // Display an error message if there's an error reading the file
      document.getElementById("error-message").textContent =
        "Error reading file. Please try again.";
    }
  }

  async function validateNumber(number) {
    try {
      // Make AJAX request to validate the number in the file
      const validationResponse = await fetch(
        `/api/validate-number?number=${number}`
      );
      const validationData = await validationResponse.json();

      // Display the validation result
      console.log(validationData);

      // If you want to update the UI with the validation result, you can do it here
      // For example, you can create a new row in the table and populate it with validation details
      const tableBody = document.getElementById("validation-table-body");
      const newRow = document.createElement("tr");

      // Create cells for phone number and details
      const phoneNumberCell = document.createElement("td");
      phoneNumberCell.textContent = number;
      newRow.appendChild(phoneNumberCell);

      // Create cells for validation details
      const numberType = document.createElement("td");
      numberType.textContent = validationData.number_type || "unknown";
      newRow.appendChild(numberType);

      const isValid = document.createElement("td");
      isValid.textContent = validationData.is_valid || "unknown";
      newRow.appendChild(isValid);

      const carrier = document.createElement("td");
      carrier.textContent = validationData.carrier || "unknown";
      newRow.appendChild(carrier);

      const country = document.createElement("td");
      country.textContent = validationData.country || "unknown";
      newRow.appendChild(country);

      const regionName = document.createElement("td");
      regionName.textContent = validationData.region_name || "unknown";
      newRow.appendChild(regionName);

      const city = document.createElement("td");
      city.textContent = validationData.city || "unknown";
      newRow.appendChild(city);

      const zipCode = document.createElement("td");
      zipCode.textContent = validationData.zip_code || "unknown";
      newRow.appendChild(zipCode);

      // Append the new row to the table body
      tableBody.appendChild(newRow);
    } catch (error) {
      console.error("Error validating number:", error);
    }
  }

  stateSelect.addEventListener("change", function () {
    const selectedState = stateSelect.value;
    if (selectedState === "random") {
      citySelect.disabled = true;
      areaCodeSelect.disabled = true;
    } else {
      fetch(`/api/cities?state=${selectedState}`)
        .then((response) => response.json())
        .then((data) => {
          citySelect.innerHTML = "";
          const cityPlaceholderOption = document.createElement("option");
          cityPlaceholderOption.value = "";
          cityPlaceholderOption.textContent = "Random";
          citySelect.appendChild(cityPlaceholderOption);
          data.cities.forEach((city) => {
            const option = document.createElement("option");
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
          });
          citySelect.disabled = false;
          areaCodeSelect.disabled = true;
        })
        .catch((error) => {
          console.error("Error fetching cities and area codes:", error);
        });
    }
  });

  citySelect.addEventListener("change", function () {
    const selectedCity = citySelect.value;
    if (selectedCity !== "") {
      fetch(`/api/area-codes?city=${selectedCity}`)
        .then((response) => response.json())
        .then((data) => {
          areaCodeSelect.innerHTML = "";
          const areaCodePlaceholderOption = document.createElement("option");
          areaCodePlaceholderOption.value = "";
          areaCodePlaceholderOption.textContent = "Random";
          areaCodeSelect.appendChild(areaCodePlaceholderOption);
          data.areaCodes.forEach((code) => {
            const option = document.createElement("option");
            option.value = code;
            option.textContent = code;
            areaCodeSelect.appendChild(option);
          });
          areaCodeSelect.disabled = false;
        })
        .catch((error) => {
          console.error("Error fetching area codes:", error);
        });
    } else {
      areaCodeSelect.innerHTML = "";
      const areaCodePlaceholderOption = document.createElement("option");
      areaCodePlaceholderOption.value = "";
      areaCodePlaceholderOption.textContent = "Random";
      areaCodeSelect.appendChild(areaCodePlaceholderOption);
      areaCodeSelect.disabled = true;
    }
  });

  // Event listener for the generate button
  const validateBtn = document.getElementById("validate-btn");
  validateBtn.addEventListener("click", async function () {
    await validateNumbers();
  });

  async function validateNumbers() {
    // Fetch selected state, city, area code, and quantity
    const selectedState = stateSelect.value;
    const selectedCity = citySelect.value;
    const selectedAreaCode = areaCodeSelect.value;
    const numOfNumbers = document.getElementById("num-of-numbers").value;

    // Make AJAX request to get random numbers
    const numbersResponse = await fetch(
      `/api/get-random-numbers?state=${selectedState}&city=${selectedCity}&area_code=${selectedAreaCode}&numOfNumbers=${numOfNumbers}`
    );
    const numbersData = await numbersResponse.json();

    // Clear previous data from table body
    const tableBody = document.getElementById("validation-table-body");
    tableBody.innerHTML = "";

    // Iterate over each generated number
    for (const number of numbersData.numbers) {
      try {
        // Make AJAX request to validate the number
        const validationResponse = await fetch(
          `/api/validate-number?number=${number}`
        );
        const validationData = await validationResponse.json();

        // Create a new row for the table
        const newRow = document.createElement("tr");

        // Create cells for phone number and details
        const phoneNumberCell = document.createElement("td");
        phoneNumberCell.textContent = number;
        newRow.appendChild(phoneNumberCell);

        // Create cells for validation details
        const numberType = document.createElement("td");
        numberType.textContent = validationData.number_type || "unknown";
        newRow.appendChild(numberType);

        const isValid = document.createElement("td");
        isValid.textContent = validationData.is_valid || "unknown";
        newRow.appendChild(isValid);

        const carrier = document.createElement("td");
        carrier.textContent = validationData.carrier || "unknown";
        newRow.appendChild(carrier);

        const country = document.createElement("td");
        country.textContent = validationData.country || "unknown";
        newRow.appendChild(country);

        const regionName = document.createElement("td");
        regionName.textContent = validationData.region_name || "unknown";
        newRow.appendChild(regionName);

        const city = document.createElement("td");
        city.textContent = validationData.city || "unknown";
        newRow.appendChild(city);

        const zipCode = document.createElement("td");
        zipCode.textContent = validationData.zip_code || "unknown";
        newRow.appendChild(zipCode);

        // Append the new row to the table body
        tableBody.appendChild(newRow);
      } catch (error) {
        console.error("Error validating number:", error);
      }
    }
  }
});
