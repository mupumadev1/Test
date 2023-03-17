const processBtn = document.getElementById('process-btn');
const searchResultsTable = document.getElementById('table-body');
const searchVendorInput = document.getElementById('search-vendor-id');
const modalSubmitBtn = document.getElementById('modal-submit-btn');

var searchResults = document.getElementById('search-results');
var checkboxes = document.querySelectorAll('input[type="checkbox"]');

var selectedVendorsInvoiceNumber = [];

// Add selected vendors to array
function addselectedVendorsInvoiceNumber(invoiceId) {
  // Check if invoice id is already in array
  if (!selectedVendorsInvoiceNumber.includes(invoiceId)) {
    selectedVendorsInvoiceNumber.push(invoiceId);
  }
}

// function to add event listener to checkboxes that checks if they are checked or not
function addEventListenerToCheckboxes(checkboxes) {
  // Add event listener to checkboxes
  checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      // Check if checkbox is checked
      if (cb.checked) {
        // Add vendor id to array
        addselectedVendorsInvoiceNumber(cb.value);
      } else {
        // Remove vendor id from array
        selectedVendorsInvoiceNumber = selectedVendorsInvoiceNumber.filter(vendor => vendor !== cb.value);
      }
      
      // Check if at least one checkbox is checked and disable button if none is checked
      const isChecked = Array.from(checkboxes).some(cb => cb.checked);
      if (!isChecked) {
        processBtn.disabled = true;
      } else {    
        processBtn.disabled = false;
      }

    });
  });
}

/* Function to change checkbox to checked if vendor id 
is in array and new table results are dispalyed */
function checkCheckboxIfVendorIdIsInArray(checkboxes) { 
  checkboxes.forEach(cb => {
    if (selectedVendorsInvoiceNumber.includes(cb.value)) {
      cb.checked = true;
    }
  });
}

/* Function that takes the vendor_info and transaction_info
   and returns the html table body elements  */
function createTableBody(transactionInfo, vendorInfo, tableBodyID) {
  // Get table body element
  const tableBody = document.getElementById(tableBodyID);
  tableBody.innerHTML = '';
  // Create new html form elements and add csrf_token
  const searchResultsTableForm = document.createElement('form');
  searchResultsTableForm.method = 'POST';
  searchResultsTableForm.innerHTML = '{% csrf_token %}'

  // Add new transactions
  transactionInfo.forEach(transaction => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <input type="checkbox" name="transaction" value="${transaction.idinvc}">
      </td>
      <td>${transaction.datermit}</td>
      <td>${transaction.amtpaym}</td>
      <td>${transaction.codecurn}</td>
      <td>${transaction.idinvc}</td>
      <td>${transaction.idvend}</td>
      `;
      vendorInfo.forEach(vendor => {
      if (transaction.idvend === vendor.vendorid) {
        tr.innerHTML += `
          <td>${vendor.accname}</td>
          <td>${vendor.accno}</td>
          <td>${vendor.bsbno}</td>
        `
      }
    });
    tableBody.appendChild(tr);
  })

}


// Add event listener to checkboxes
addEventListenerToCheckboxes(checkboxes);

// Add event listener to search vendor_id input
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
            // Add new transactions
            createTableBody(transactions.transaction_info, transactions.vendor_info, 'table-body');

             // Add event listener to checkboxes
             checkboxes = document.querySelectorAll('input[type="checkbox"]');
             addEventListenerToCheckboxes(checkboxes);
             checkCheckboxIfVendorIdIsInArray(checkboxes);
          });

        });
      });

    } else {
      //hide select element
      searchResults.classList.add('d-none');
    }
  });
}) 

// Get csrf token from cookie
const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

// Add Event Listener to process button
processBtn.addEventListener('click', (e) => {
  // Prevent Defualt Behavior
  e.preventDefault();

  // Get post transaction modal & modal table body
  const postTransactionModal = document.getElementById('post-transaction-model');
  const postTransactionModalTableBody = document.getElementById('post-transaction-modal-table-body');

  postTransactionModal.classList.add('show');

  // Send selected invoice numbers to server using ajax
  $.ajax({
    type: 'POST',
    url: 'search-invoices/',
    data: {
      'csrfmiddlewaretoken': csrfToken,
      'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
    },
    dataType: 'json',
  }).then(transactions => {
    createTableBody(transactions.transaction_info, transactions.vendor_info, 'modal-table-body');
    console.log(transactions.transaction_info);
    // Add event listener to checkboxes
    checkboxes = document.querySelectorAll('input[type="checkbox"]');
    addEventListenerToCheckboxes(checkboxes);
    checkCheckboxIfVendorIdIsInArray(checkboxes);
  }).catch(err => console.log(err));
  
});

// Add event listener to modal submit button
modalSubmitBtn.addEventListener('click', (e) => {
  e.preventDefault();

  // Send selected invoice numbers to server using ajax
  $.ajax({
    type: 'POST',
    url: 'post-transactions/',
    data: {
      'csrfmiddlewaretoken': csrfToken,
      'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
    },
    dataType: 'json',
  }).then(res => {
    console.log(res);
  })

});