document.addEventListener('DOMContentLoaded', function () {
    const stateSelect = document.getElementById('state-select');
    const citySelect = document.getElementById('city-select');
    const areaCodeSelect = document.getElementById('area-code-select');

    stateSelect.addEventListener('change', function () {
        const selectedState = stateSelect.value;
        if (selectedState === 'random') {
            citySelect.disabled = true;
            areaCodeSelect.disabled = true;
        } else {
            // Make a request to your backend to fetch cities and area codes based on the selected state
            // You can use AJAX (e.g., fetch API or XMLHttpRequest) to make the request
            fetch(`/api/cities?state=${selectedState}`) // Replace this URL with your actual endpoint
                .then(response => response.json())
                .then(data => {
                    // Populate city select with fetched cities
                    citySelect.innerHTML = '';
                    // Add placeholder option for city
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

                    // Populate area code select with fetched area codes
                    areaCodeSelect.innerHTML = '';
                    // Add placeholder option for area code
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
                    console.error('Error fetching cities and area codes:', error);
                });
        }
    });
});
