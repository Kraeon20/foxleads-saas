document.addEventListener('DOMContentLoaded', function () {
    const stateSelect = document.getElementById('state-select');
    const citySelect = document.getElementById('city-select');
    const areaCodeSelect = document.getElementById('area-code-select');
    const generateBtn = document.getElementById('generate-btn');
    const generatedNumbersDiv = document.getElementById('generated-numbers');

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
});