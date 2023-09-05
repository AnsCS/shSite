// THeam Dark and Light

// Change the theme according to the user's preference
// if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
//     document.body.classList.add('dark-theme');
// } else {
//     document.body.classList.remove('dark-theme');
// }

// document.querySelectorAll('[data-bs-theme-value]').forEach(function (el) {
//     el.addEventListener('click', function () {
//         var theme = this.getAttribute('data-bs-theme-value');
//         // Change the theme according to the selected value
//         if (theme === 'light') {
//             // Change the theme to light
//             document.body.classList.remove('dark-theme');
//         } else if (theme === 'dark') {
//             // Change the theme to dark
//             document.body.classList.add('dark-theme');
//         } else {
//             // Change the theme according to the user's preference
//             if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
//                 document.body.classList.add('dark-theme');
//             } else {
//                 document.body.classList.remove('dark-theme');
//             }
//         }
//     });
// });


// Change the theme according to the user's preference or the saved value in localStorage
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-theme');
} else if (localStorage.getItem('theme') === 'light') {
    document.body.classList.remove('dark-theme');
} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.body.classList.add('dark-theme');
} else {
    document.body.classList.remove('dark-theme');
}

document.querySelectorAll('[data-bs-theme-value]').forEach(function (el) {
    el.addEventListener('click', function () {
        var theme = this.getAttribute('data-bs-theme-value');
        // Change the theme according to the selected value
        if (theme === 'light') {
            // Change the theme to light
            document.body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        } else if (theme === 'dark') {
            // Change the theme to dark
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            // Change the theme according to the user's preference
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-theme');
                localStorage.setItem('theme', 'light');
            }
        }
    });
});

// comment in Blgo page / Add JavaScript to validate the form and reCAPTCHA

document.getElementById('comment-form').addEventListener('submit', function (event) {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var body = document.getElementById('body').value;
    if (name === "" || email === "" || body === "") {
        event.preventDefault();
        document.getElementById('validation-error').style.display = 'block';
    } else if (grecaptcha.getResponse() === "") {
        event.preventDefault();
        document.getElementById('recaptcha-error').style.display = 'block';
    }
});

// End of JavaScript validation

function formatTimestamp(timestamp) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    };
    return new Intl.DateTimeFormat(navigator.language, options).format(timestamp);
}

document.addEventListener("DOMContentLoaded", function () {
    const commentTimestamps = document.querySelectorAll(".comment-timestamp");

    for (const timestampElement of commentTimestamps) {
        const timestampUTC = new Date(timestampElement.dataset.timestamp);
        timestampElement.textContent = formatTimestamp(timestampUTC);
    }
});

// copy for code
function copyCode() {
    // Get the code text
    var code = document.getElementById("code-block").innerText;

    // Copy the code text to the clipboard
    navigator.clipboard.writeText(code);

    // Show the confirmation message
    document.getElementById("copy-message").style.display = "inline";

    // Hide the confirmation message after 2 seconds
    setTimeout(function () {
        document.getElementById("copy-message").style.display = "none";
    }, 2000);
}

// Splide card

var elms = document.getElementsByClassName( 'splide' );


for ( var i = 0; i < elms.length; i++ ) {
  new Splide( elms[ i ] ,{
    type   : 'loop',
  }).mount();
}

