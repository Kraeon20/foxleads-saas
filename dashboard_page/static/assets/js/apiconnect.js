// Define the updateTable function globally
function updateTable(data) {
    const table = document.querySelector('.validation-table');
    const tbody = table.querySelector('tbody');

    // Create a new row
    const newRow = document.createElement('tr');

    // Define the required fields and their default values
    const fields = ['phone_number', 'is_valid', 'line_type', 'carrier', 'is_prepaid'];
    const defaults = { phone_number: 'N/A', is_valid: 'N/A', line_type: 'N/A', carrier: 'N/A', is_prepaid: 'N/A' };

    // Populate the row with data
    newRow.innerHTML = fields.map(field => `<td>${data[field] || defaults[field]}</td>`).join('');

    // Append the new row to the table body
    tbody.appendChild(newRow);

    // Add the person's full name if available
    if (data.belongs_to && data.belongs_to.name) {
        const nameRow = document.createElement('tr');
        nameRow.innerHTML = `<td colspan="5"><strong>Belongs to:</strong> ${data.belongs_to.name}</td>`;
        tbody.appendChild(nameRow);
    }
}

// Define the updateTable function globally
function updateTable(data) {
    const table = document.querySelector('.validation-table');
    const tbody = table.querySelector('tbody');

    // Check if the tbody exists, if not, create it
    if (!tbody) {
        console.error('Table body does not exist');
        return;
    }

    // Create a new row
    const newRow = document.createElement('tr');

    // Define the required fields and their default values
    const fields = ['phone_number', 'is_valid', 'line_type', 'carrier', 'is_prepaid'];
    const defaults = { phone_number: 'N/A', is_valid: 'N/A', line_type: 'N/A', carrier: 'N/A', is_prepaid: 'N/A' };

    // Populate the row with data
    newRow.innerHTML = fields.map(field => `<td>${data[field] || defaults[field]}</td>`).join('');

    // Append the new row to the table body
    tbody.appendChild(newRow);

    // Add the person's full name if available
    if (data.belongs_to && data.belongs_to.name) {
        const nameRow = document.createElement('tr');
        nameRow.innerHTML = `<td colspan="5"><strong>Belongs to:</strong> ${data.belongs_to.name}</td>`;
        tbody.appendChild(nameRow);
    }
}
