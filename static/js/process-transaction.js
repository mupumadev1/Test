const processBtn = document.getElementById('process-btn');
const searchBtn = document.getElementById('search-btn');
const modalSubmitBtn = document.getElementById('modal-submit-btn');

const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const searchInput = document.getElementById('search-input');
const filterOptions = document.getElementById('filter-options');

const nextPageLink = document.getElementById('next');
const lastPageLink = document.getElementById('last');
const previousPageLink = document.getElementById('previous');
const firstPageLink = document.getElementById('first');
const currentPage = document.getElementById('current');

let selectedVendorsInvoiceNumber = [];
let selectedPageNumber = 1;
let numberOfPages = 0;
let hasClickedOnSearchBtn = false;
let query_params = [];


function addSelectedVendorsInvoiceNumber(invoiceId) {
  /**
   * Add selected vendors to array
   */
  if (!selectedVendorsInvoiceNumber.includes(invoiceId)) {
    selectedVendorsInvoiceNumber.push(invoiceId);
  }
}

let selectedTransactionType = {}

 /**
     * Saves selected transaction type for a particular transaction in selectedTransactionType Objects DS
     * @param {String} invoiceNumber - Invoice Number for Selected Transaction
     * @param {String} transactionType - Transaction Type E.g. NFS, RTGS or DDUC
     * @throws {Error} - If transaction type is invalid
     * */
function saveSelectedTransactionType(invoiceNumber, transactionType) {


    const validTransactionTypes = new Set(["NFS", "RTGS", "DDUC" ]);
    if (validTransactionTypes.has(transactionType) )  {
       selectedTransactionType[invoiceNumber] = transactionType;
    } else {
        throw new Error('Invalid Transaction Type');
    }
}

/** loops through the rows of a table and saves the selected transaction
 * types in an object called selectedTransactionType.
 * @param {String} tableID - ID for Table
 * */
function saveSelectedRows(tableID) {
    let rows = document.querySelectorAll(`#${tableID} tr`);

    rows.forEach((row) => {
        let cb = row.querySelector('td input[type="checkbox"]')
        if(cb.checked) {
           let transactionType = row.querySelector('td select[name="transaction_type"]').value;
           saveSelectedTransactionType(cb.value, transactionType);
        }
      }
    )
}

function updateTransactionType(tableID) {
    let rows = document.querySelectorAll(`#${tableID} tr`);

    rows.forEach((row) => {
        let cb = row.querySelector('td input[type="checkbox"]');
        let invoiceID = cb.value;
        if(isTransactionTypeSaved(invoiceID)) {
           let transactionType = row.querySelector('td select[name="transaction_type"]');
           transactionType.value = selectedTransactionType[invoiceID]
        }
      }
    )
}

/** Check if Transaction type is in selectedTransactionType
 * @param {String} invoiceID - Invoice ID for a particular transaction
 * @return {Boolean}
 * */
function isTransactionTypeSaved(invoiceID) {
    return invoiceID in selectedTransactionType;
}

/** Adds Event Listener to Select Transactions DropDown That Listens for Change Events
 * If value of Dropdown has changed,then save transaction type
 */
function addEventListenerToSelectTransactionType() {
    const selectTransactionTypeFields = document.querySelectorAll('.custom-select');

    for (let selectTransactionTypeField of selectTransactionTypeFields) {
        selectTransactionTypeField.addEventListener('change', () => {
            saveSelectedRows('table-body');
        })
    }
}

 /**
   * Add event listener to checkboxes
   */
function addEventListenerToCheckboxes(checkboxes) {

  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked) {
        // Add vendor id to array
        addSelectedVendorsInvoiceNumber(cb.value);
        saveSelectedRows('table-body')
      } else {
        // Remove vendor id from array
        selectedVendorsInvoiceNumber = selectedVendorsInvoiceNumber.filter(vendor => vendor !== cb.value);
      }
      
      // Check if at least one checkbox is checked and disable button if none is checked
      const isChecked = Array.from(checkboxes).some(cb => cb.checked);
      processBtn.disabled = !isChecked;

    });
  });
}

function checkCheckboxIfVendorIdIsInArray(checkboxes) {
  /**
   * Check if vendor id is in array and change checkbox to checked if it is
   */
  checkboxes.forEach(cb => {
    if (selectedVendorsInvoiceNumber.includes(cb.value)) {
      cb.checked = true;
    }
  });
}

function getCheckboxes() {
    /**
     *  Get all checkboxes, add event listener to them and check if they are checked or not
     */
    let checkboxes = document.querySelectorAll('input[type="checkbox"]');
    addEventListenerToCheckboxes(checkboxes);
    checkCheckboxIfVendorIdIsInArray(checkboxes);
}

/** Create new table body elements and add them to the table body
    * @param {Array} transactionInfo - Array of transaction objects
    * @param {Array} vendorInfo - Array of vendor objects
    * @param {String} tableBodyID - ID of table body element  */
function createTableBody(transactionInfo, vendorInfo, tableBodyID) {
  let tableBody = document.getElementById(tableBodyID);
  tableBody.innerHTML = '';

  // Add new transactions
  if (transactionInfo.length > 0) {
    for (let transaction of transactionInfo) {
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

      for (let vendor of vendorInfo) {
        if (transaction.idvend === vendor.vendorid) {
          tr.innerHTML += `
            <td>${ vendor.accname }</td>
            <td>${vendor.accno }</td>
            <td>${vendor.bsbno }</td>
          `;
        }
      }

      tr.innerHTML += `
         <td>
            <select class="custom-select" name="transaction_type">
            <option value="DDUC">DDUC</option>
            <option value="NFS">NFS</option>
            <option value="RTGS">RTGS</option>
            </select>
        </td>
      `;

      tableBody.appendChild(tr);
    }

  } else {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td colspan="8" class="text-center">No transactions found</td>
    `;

    tableBody.appendChild(tr);
  }

  updateTransactionType(tableBodyID);

}

/** Check if page has next or previous page */
function checkIfPageHasNextOrPreviousPage() {
  if (selectedPageNumber === 1) {
    previousPageLink.classList.add('d-none');
    if (numberOfPages === 1) {
      nextPageLink.classList.add('d-none');
    }
  } else {
    previousPageLink.classList.remove('d-none');
  }

  if (selectedPageNumber === numberOfPages) {
    nextPageLink.classList.add('d-none');
  } else {
    nextPageLink.classList.remove('d-none');
  }
}

function nextPage() {
  /**
   *  Go to next page
   */
  if (selectedPageNumber !== numberOfPages) {
    selectedPageNumber += 1;
  }

  goToPage(`search/`, 'table-body');

}

function previousPage() {
  /**
   *  Go to previous page
   */
  if (selectedPageNumber !== 1) {
    selectedPageNumber -= 1;
  }

  goToPage(`search/`, 'table-body');
}

function checkIfLastPage() {
  /**
   * Check If the selected page is the last page
   * */

   if (selectedPageNumber === numberOfPages) {
    lastPageLink.classList.add('d-none');
  } else {
    lastPageLink.classList.remove('d-none');
  }

}



function checkIfFirstPage(){
  /**
   * Check if the selected page is the first page
   * */
    if (selectedPageNumber === 1) {
        firstPageLink.classList.add('d-none');
    } else {
        firstPageLink.classList.remove('d-none');
    }
}

async function goToPage(url, tbodyID) {
  /**
   *  Get New Paginated Page Data, Pagination Page Number and Number of Pages
   *  @param {String} url - URL to send ajax request to
   *  @param {String} tbody - ID of table body element
   */

  currentPage.textContent = `Page ${selectedPageNumber} of ${numberOfPages}.`;

  checkIfFirstPage();
  checkIfLastPage();
  checkIfPageHasNextOrPreviousPage();

  try {
    // Send ajax request to server to retrieve new paginated data
    const res = await fetch(`${url}?search_params=${query_params[0]}&filter_options=${query_params[1]}&page_number=${selectedPageNumber}`);
    const data = await res.json();
    const transactionInfo = data.transaction_info;
    const vendorInfo = data.vendor_info;

    // Create new table body
    createTableBody(transactionInfo, vendorInfo, tbodyID, 'goToPage Function');
    getCheckboxes();

    updateTransactionType(tbodyID);
  } catch (err) {
    console.log(err);
  }
}

async function searchDatabase(searchParams, filterOptions) {
  /**
   * Send request to database to search for vendor transactions
   * and vendor information that matches the search parameters
   * @param {String} searchParams - String containing search parameters
   * @param {String} filterOptions - String containing filter options
   * @return {Array} - Object containing transaction info and vendor info
   * */

      // Send ajax request to server to retrieve matching vendors
  const res = await fetch(`search/?search_params=${searchParams}&filter_options=${filterOptions}&page_number=1`);

  return await res.json();
}

// Add event listener to checkboxes
addEventListenerToCheckboxes(checkboxes);
addEventListenerToSelectTransactionType();

// add event listener to search btn
searchBtn.addEventListener('click', (e) => {
  e.preventDefault();
  hasClickedOnSearchBtn = true;

  // Query the database for the specified search parameters
  let queryResults = searchDatabase(searchInput.value, filterOptions.value);

  // Display the results in the table body
    queryResults.then((data) => {
        createTableBody(data.transaction_info, data.vendor_info, 'table-body');
        getCheckboxes();
        addEventListenerToSelectTransactionType();
        numberOfPages = data.number_of_pages;
        currentPage.textContent = `Page 1 of ${numberOfPages}.`;
        query_params = [searchInput.value, filterOptions.value]
        checkIfPageHasNextOrPreviousPage();

    }).catch((err) => {
      console.log(err)
    });
});

// Add event listener to change page links
nextPageLink.addEventListener('click', (e) => {
  if (hasClickedOnSearchBtn === true) {
    e.preventDefault();
    nextPage();
  }
});

previousPageLink.addEventListener('click', (e) => {
    if (hasClickedOnSearchBtn === true) {
        e.preventDefault();
        previousPage();
    }
});

lastPageLink.addEventListener('click', (e) => {
  if (hasClickedOnSearchBtn === true) {
    e.preventDefault();
    selectedPageNumber = numberOfPages;
    goToPage(`get-vendor-transactions/`, 'table-body');
  }
});

firstPageLink.addEventListener('click', (e) => {
  if (hasClickedOnSearchBtn === true){
    e.preventDefault();
    selectedPageNumber = 1;
   goToPage(`get-vendor-transactions/`, 'table-body');
  }
});

function getCSRFToken() {
    let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    if (csrfToken == null) {
        csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }
    return csrfToken;
}


// Add Event Listener to process button
processBtn.addEventListener('click', (e) => {
  e.preventDefault();

  $.ajax({
    type: 'POST',
    url: 'search-invoices/',
    data: {
      'csrfmiddlewaretoken': getCSRFToken(),
      'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
    },
    dataType: 'json',
  }).then(transactions => {
    createTableBody(transactions.transaction_info, transactions.vendor_info, 'modal-table-body');
    // Add event listener to checkboxes
    getCheckboxes();
    addEventListenerToSelectTransactionType();

    updateTransactionType('modal-table-body');
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
      'csrfmiddlewaretoken': getCSRFToken(),
      'invoice_ids[]': JSON.stringify(selectedVendorsInvoiceNumber),
      'transaction_type': JSON.stringify(selectedTransactionType),
    },
    dataType: 'json',
  }).then(res => {
    console.log(res);
  })

});