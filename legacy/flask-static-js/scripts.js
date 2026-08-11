// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Handle Welcome Message Overlay
    const welcomeMessage = document.getElementById('welcome-message');
    if (welcomeMessage) {
        // Show the welcome message
        welcomeMessage.style.display = 'flex';

        // Hide after 7 seconds
        const hideTime = 5000; // 5000 ms = 5 seconds
        setTimeout(() => {
            welcomeMessage.classList.add('hidden');
            // Optionally remove the element after the transition
            setTimeout(() => {
                welcomeMessage.style.display = 'none';
            }, 2000); // Match the CSS transition duration
        }, hideTime);
    }

    // Dynamic Region Message
    const dynamicMessageElement = document.getElementById('dynamic-region-message');
    if (dynamicMessageElement) {
        const messages = JSON.parse(dynamicMessageElement.getAttribute('data-messages')) || [];
        let currentIndex = 0;

        function changeDynamicMessage() {
            // Fade out the current message
            dynamicMessageElement.style.opacity = '0';

            // After fade out transition, change the message and fade in
            setTimeout(() => {
                currentIndex = (currentIndex + 1) % messages.length;
                dynamicMessageElement.textContent = messages[currentIndex];
                // Fade in the new message
                dynamicMessageElement.style.opacity = '1';
            }, 1000); // Match the CSS transition duration
        }

        // Initialize opacity for transitions
        dynamicMessageElement.style.transition = 'opacity 1s ease';
        dynamicMessageElement.style.opacity = '1';

        // Start the interval to change messages every 15 seconds
        setInterval(changeDynamicMessage, 15000); // 15000 ms = 15 seconds
    }

    // Handle Dynamic Top Message
    const dynamicTopMessageElement = document.getElementById('dynamic-top-message');
    if (dynamicTopMessageElement) {
        const messages = JSON.parse(dynamicTopMessageElement.getAttribute('data-messages')) || [];
        let currentIndex = 0;

        function changeTopMessage() {
            if (messages.length === 0) return;

            // Fade out
            dynamicTopMessageElement.classList.remove('show');

            // After fade out transition, change the message and fade in
            setTimeout(() => {
                // Select a random message
                currentIndex = Math.floor(Math.random() * messages.length);
                dynamicTopMessageElement.textContent = messages[currentIndex];
                // Fade in the new message
                dynamicTopMessageElement.classList.add('show');
            }, 1000); // Match the CSS transition duration
        }

        // Initial fade in
        dynamicTopMessageElement.classList.add('show');

        // Change message every 40 seconds
        setInterval(changeTopMessage, 10000); // 40000 ms = 40 seconds
    }

    // Bootstrap form validation
    (function () {
        'use strict'
        var forms = document.querySelectorAll('.needs-validation')
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
    })()
});
