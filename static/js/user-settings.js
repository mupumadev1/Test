var changePasswordBtn = document.querySelector('#change-password-btn');
var closeBtn = document.querySelector('#close-change-password-btn');
var passwordInput = document.querySelector('#password');
var submitPasswordBtn = document.querySelector('#submit-change-password-btn');

changePasswordBtn.addEventListener('click', () => {
    passwordInput.disabled = false;
    submitPasswordBtn.classList.remove('d-none');

    const hiddenInputs = document.querySelectorAll('.d-none');
    hiddenInputs.forEach(input => {
        input.classList.remove('d-none');
        input.classList.add('chg-password');
    });

    changePasswordBtn.classList.add('d-none');
});

closeBtn.addEventListener('click', () => {
    passwordInput.disabled = true;
    submitPasswordBtn.classList.add('d-none');

    const visibleInputs = document.querySelectorAll('.chg-password');
    visibleInputs.forEach(input => {
        input.classList.add('d-none');
        input.classList.remove('chg-password');
    });

    changePasswordBtn.classList.remove('d-none');
});


function showPassword(id) {
    var input = document.getElementById(id);
    var link = input.nextElementSibling;

    if (input.type === "password") {
        input.type = "text";
        link.textContent = "Hide Password";
    } else {
        input.type = "password";
        link.textContent = "Show Password";
    }
    
}
