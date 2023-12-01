const cashfree = Cashfree({
    mode:"sandbox" //or production
});

// multi select

const dropdownButton = document.getElementById('multiSelectDropdown');
const courselist = document.getElementById('course_list');
const dropdownMenu = document.querySelector('.dropdown-menu');
let mySelectedItems = [];

function handleCB(event) {
    const checkbox = event.target;

    if (checkbox.value === 'all') {
        const allCheckboxes = document.querySelectorAll('.dropdown-menu input[type="checkbox"]');
        if (checkbox.checked) {
            mySelectedItems = Array.from(allCheckboxes)
                .filter(item => item !== checkbox)
                .map(item => item.value);
        } else {
            mySelectedItems = [];
        }

        allCheckboxes.forEach(item => {
            item.checked = checkbox.checked;
        });
    } else {
        if (checkbox.checked) {
            mySelectedItems.push(checkbox.value);
        } else {
            mySelectedItems = mySelectedItems.filter((item) => item !== checkbox.value);
        }

        const allCheckbox = document.querySelector('.dropdown-menu input[value="all"]');
        allCheckbox.checked = Array.from(dropdownMenu.querySelectorAll('input[type="checkbox"]:not([value="all"])')).every(item => item.checked);
    }

    dropdownButton.value = mySelectedItems.join(', ');
    courselist.value = mySelectedItems;
}

dropdownMenu.addEventListener('click', handleCB);

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('Send').addEventListener('click', function (event) {
        var confirmation = window.confirm('Are you sure?');
        if (!confirmation) {
            event.preventDefault();
        } else {
            document.querySelector('.form').submit();
        }
    });
});

let textarea = document.getElementById('mytextarea')
let messagebox = document.getElementById('message')

function for_email_message() {
    var message = textarea.value;
    messagebox.value = message;
}

textarea.addEventListener('keyup', for_email_message)
