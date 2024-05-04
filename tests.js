document.addEventListener('DOMContentLoaded', function () {
  const stateSelect = document.getElementById('state-select');
  const citySelect = document.getElementById('city-select');
  const areaCodeSelect = document.getElementById('area-code-select');
  const generateBtn = document.getElementById('generate-btn');
  const generatedNumbersDiv = document.getElementById('generated-numbers');
  const exportTxtBtn = document.getElementById('export-txt-btn'); 
  const exportCsvBtn = document.getElementById('export-csv-btn'); 
  const exportJsonBtn = document.getElementById('export-json-btn');
  const exportOptions = document.querySelector('.export-options');
  const exportBtn = document.getElementById('export-btn');  // Define exportBtn variable
  const exportOptionsBtn = document.getElementById('export-options-btn');


  stateSelect.addEventListener('change', function () {
      const selectedState = stateSelect.value;
      if (selectedState === 'random') {
          citySelect.disabled = true;
          areaCodeSelect.disabled = true;
      } else {
          fetch(`/api/cities?state=${selectedState}`)
              .then(response => response.json())
              .then(data => {
                  citySelect.innerHTML = '';
                  const cityPlaceholderOption = document.createElement('option');
                  cityPlaceholderOption.value = '';
                  cityPlaceholderOption.textContent = 'Select a City';
                  citySelect.appendChild(cityPlaceholderOption);
                  data.cities.forEach(city => {
                      const option = document.createElement('option');
                      option.value = city;
                      option.textContent = city;
                      citySelect.appendChild(option);
                  });
                  citySelect.disabled = false;
                  areaCodeSelect.disabled = true;
              })
              .catch(error => {
                  console.error('Error fetching cities and area codes:', error);
              });
      }
  });

  citySelect.addEventListener('change', function () {
      const selectedCity = citySelect.value;
      if (selectedCity !== '') {
          fetch(`/api/area-codes?city=${selectedCity}`)
              .then(response => response.json())
              .then(data => {
                  areaCodeSelect.innerHTML = '';
                  const areaCodePlaceholderOption = document.createElement('option');
                  areaCodePlaceholderOption.value = '';
                  areaCodePlaceholderOption.textContent = 'Select an Area Code';
                  areaCodeSelect.appendChild(areaCodePlaceholderOption);
                  data.areaCodes.forEach(code => {
                      const option = document.createElement('option');
                      option.value = code;
                      option.textContent = code;
                      areaCodeSelect.appendChild(option);
                  });
                  areaCodeSelect.disabled = false;
              })
              .catch(error => {
                  console.error('Error fetching area codes:', error);
              });
      } else {
          areaCodeSelect.innerHTML = '';
          const areaCodePlaceholderOption = document.createElement('option');
          areaCodePlaceholderOption.value = '';
          areaCodePlaceholderOption.textContent = 'Select an Area Code';
          areaCodeSelect.appendChild(areaCodePlaceholderOption);
          areaCodeSelect.disabled = true;
      }
  });

  generateBtn.addEventListener('click', function () {
      const selectedState = stateSelect.value;
      const selectedCity = citySelect.value;
      const selectedAreaCode = areaCodeSelect.value;
      const numOfNumbers = parseInt(document.getElementById('num-of-numbers').value);

      fetch(`/api/generate-numbers?state=${selectedState}&city=${selectedCity}&area_code=${selectedAreaCode}&numOfNumbers=${numOfNumbers}`)
          .then(response => response.json())
          .then(data => {
              const generatedNumbersDiv = document.getElementById('generated-numbers');
              generatedNumbersDiv.innerHTML = '';
              data.numbers.forEach(number => {
                  const p = document.createElement('p');
                  p.textContent = number;
                  generatedNumbersDiv.appendChild(p);
              });
          })
          .catch(error => {
              console.error('Error fetching random numbers:', error);
          });
  });

  
  // Toggle export options visibility
  exportOptionsBtn.addEventListener('click', function () {
      exportOptions.classList.toggle('active');
  });

  // Function to trigger download
  function download(filename, text) {
      const element = document.createElement('a');
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
      element.setAttribute('download', filename);

      element.style.display = 'none';
      document.body.appendChild(element);

      element.click();

      document.body.removeChild(element);
  }

  // Add event listener for export TXT button
  exportTxtBtn.addEventListener('click', function () {
      const generatedNumbers = [...generatedNumbersDiv.querySelectorAll('p')].map(p => p.textContent);
      download('generated_numbers.txt', generatedNumbers.join('\n'));
      exportOptions.classList.remove('active'); // Hide export options after selection
  });

  // Add event listener for export CSV button
  exportCsvBtn.addEventListener('click', function () {
      const generatedNumbers = [...generatedNumbersDiv.querySelectorAll('p')].map(p => p.textContent);
      download('generated_numbers.csv', generatedNumbers.join('\n'));
      exportOptions.classList.remove('active'); // Hide export options after selection
  });

  // Add event listener for export JSON button
  exportJsonBtn.addEventListener('click', function () {
      const generatedNumbers = [...generatedNumbersDiv.querySelectorAll('p')].map(p => p.textContent);
      download('generated_numbers.json', JSON.stringify({ generatedNumbers }));
      exportOptions.classList.remove('active'); // Hide export options after selection
  });

  // Add event listener for export button
  exportBtn.addEventListener('click', function () {
      // By default, download in TXT format
      const generatedNumbers = [...generatedNumbersDiv.querySelectorAll('p')].map(p => p.textContent);
      download('generated_numbers.txt', generatedNumbers.join('\n'));
  });
  
});