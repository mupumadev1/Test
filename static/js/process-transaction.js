const processBtn = document.getElementById('process-btn');
const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const searchVendorInput = document.getElementById('search-vendor-id');
var searchResults = document.getElementById('search-results');

// Add event listener to button
processBtn.addEventListener('click', function() {
  // Check if at least one checkbox is checked
  const isChecked = Array.from(checkboxes).some(cb => cb.checked);
  
  // If no checkbox is checked, disable the button
  if (!isChecked) {
    processBtn.disabled = true;
  }
});

// Add event listener to checkboxes
checkboxes.forEach(cb => {
  cb.addEventListener('change', function() {
    // Check if at least one checkbox is checked
    const isChecked = Array.from(checkboxes).some(cb => cb.checked);
    
    // If at least one checkbox is checked, enable the button
    if (isChecked) {
      processBtn.disabled = false;
    }
    // Otherwise, disable the button
    else {
      processBtn.disabled = true;
    }
  });
});

searchVendorInput.addEventListener('input', () => {
  const searchInput = searchVendorInput.value;

  // Send ajax request to server to retrieve matching vendors
  fetch(`search/?vendor_id=${searchInput}`).then(res => res.json())
  .then(options => {
    // clear existing options
    searchResults.innerHTML = '';

    // Add ul tag
    var searchResultsList = document.createElement('ul');
    searchResultsList.classList.add('list-unstyled');
    searchResultsList.id = 'search-results-list';

    // Add ul tag to search results div
    searchResults.appendChild(searchResultsList);

    // Add new options
    if (options.length > 0) {
      //show select element
      searchResults.classList.remove('d-none');
      options.forEach(option => {
        const listItm = document.createElement('li');
        const link = document.createElement('a');
        link.href = `get-vendor-transactions/?vendor_id=${option.idvend}`;
        link.textContent = option.idvend;
        listItm.appendChild(link);
        searchResultsList.appendChild(listItm);
        // Add event listener to each link
        link.addEventListener('click', (e) => {
          // Prevent default behavior
          e.preventDefault();
          // Get transactions for vendor and display results in table body
          fetch(`get-vendor-transactions/?vendor_id=${option.idvend}`).then(res => res.json())
          .then(transactions => {
            // Get table body
            const tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';
            // Add new transactions
            transactions.forEach(transaction => {
              const tr = document.createElement('tr');
              tr.innerHTML = `
                <td>${transaction.idbank}</td>
                <td>${transaction.datermit}</td>
                <td>${transaction.amtpaym}</td>
                <td>${transaction.codecurn}</td>
                <td>${transaction.rateexchhc}</td>
                <td>${transaction.paymcode}</td>
                <td>${transaction.idvend}</td>
              `;
              tableBody.appendChild(tr);
            });
          });

        });
      });

    } else {
      //hide select element
      searchResults.classList.add('d-none');
    }
  });
})


