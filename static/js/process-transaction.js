const processBtn = document.getElementById('process-btn');
var checkboxes = document.querySelectorAll('input[type="checkbox"]');
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

// function to add event listener to checkboxes
function addEventListenerToCheckboxes(checkboxes) {
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
}

// Add event listener to checkboxes
addEventListenerToCheckboxes(checkboxes);

searchVendorInput.addEventListener('input', () => {
  const searchInput = searchVendorInput.value;
  const transactionTable = document.getElementById('transaction-table');

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
        // Create list item
        const listItm = document.createElement('li');
        const link = document.createElement('a');
        link.href = `get-vendor-transactions/?vendor_id=${option.idvend}`;
        link.textContent = option.idvend;
        link.classList.add('text-dark', 'w-100', 'h-100', 'p-2');
        listItm.appendChild(link);
        searchResultsList.appendChild(listItm);

        // Add event listener to each link
        link.addEventListener('click', (e) => {
          // Prevent default behavior
          e.preventDefault();
          // Get transactions for vendor and display results in table body
          fetch(`get-vendor-transactions/?vendor_id=${option.idvend}`).then(res => res.json())
          .then(transactions => {
            // Get trasaction table body
            const searchResultsTable = document.getElementById('table-body');
            searchResultsTable.innerHTML = '';

            // Create new html form elements and add csrf_token
            const searchResultsTableForm = document.createElement('form');
            searchResultsTableForm.method = 'POST';
            searchResultsTableForm.innerHTML = '{% csrf_token %}'
            
            // Add new transactions
            transactions.forEach(transaction => {
              const tr = document.createElement('tr');
              tr.innerHTML = `
                <td>
                  <input type="checkbox" name="transaction" value="${transaction.idbank}">
                </td>
                <td>${transaction.idbank}</td>
                <td>${transaction.datermit}</td>
                <td>${transaction.amtpaym}</td>
                <td>${transaction.codecurn}</td>
                <td>${transaction.rateexchhc}</td>
                <td>${transaction.paymcode}</td>
                <td>${transaction.idvend}</td>
              `;
              searchResultsTable.appendChild(searchResultsTableForm.appendChild(tr));

              // Add event listener to checkboxes
              checkboxes = document.querySelectorAll('input[type="checkbox"]');
              addEventListenerToCheckboxes(checkboxes);

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


