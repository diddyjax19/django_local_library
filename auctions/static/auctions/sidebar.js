//wait for DOM to load before executing 
document.addEventListener("DOMContentLoaded", function(event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId);
        const nav = document.getElementById(navId);
        const bodypadding = document.getElementById(bodyId);
        const headerpadding = document.getElementById(headerId);
        const categoriesText = nav.querySelector('.nav_logo');

        // Validate that all variables exist
        if (toggle && nav && bodypadding && headerpadding) {
            toggle.addEventListener('click', () => {
                // show navbar
                nav.classList.toggle('show');
                // change icon
                toggle.classList.toggle('fa-times');
                // add padding to body
                bodypadding.classList.toggle('body-pd');
                // add padding to header
                headerpadding.classList.toggle('body-pd');
                // show categories text
                categoriesText.classList.toggle('hide-inner');
            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    // Set active link
    const color = document.querySelectorAll('.nav_link');

    function colorLink() {
        if (color) {
            color.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        }
    }
    color.forEach(l => l.addEventListener('click', color));

    // create time function
    setInterval(tellTime, 1000);

    function tellTime() {
        // instance of the date object to get hours, mins and secs
        let time = new Date();
        let hour = time.getHours();
        let minutes = time.getMinutes();
        let seconds = time.getSeconds();

        // set time of the day
        gmt = "AM";

        // works with the 24hr model, converted back to 12hr system
        if (hour > 12) {
            hour -= 12;
            gmt = "PM";
        }

        if (hour == 0) {
            hr = 12;
            gmt = "AM";
        }

        // date string
        hour = hour < 10 ? "0" + hour : hour;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        let current = hour + ":" + minutes + ":" + seconds + ":" + gmt;
        // manipulate the DOM
        document.getElementById("clock").innerHTML = current;
    }
    showTime();

});