/*
document.getElementById("register-form").addEventListener("submit", function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the values of the form inputs
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    // Perform client-side validation
    if (username === "" || password === "") {
        alert("Please fill out all fields.");
        return;  // Prevent the form from submitting
    }

    // If validation is successful, submit the form manually
    this.submit(); // This will allow the form to be submitted to the Flask server
});*/
document.getElementById('video-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const link = document.getElementById('youtube-link').value;
    const videoId = extractVideoId(link);

    if (videoId) {
        const embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&showinfo=0`;
        document.getElementById('video-container').innerHTML = `<iframe width="560" height="315" src="${embedUrl}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
        startTimer();
        document.getElementById('stop-session').style.display = 'block';  // Show the stop button
        enterFullscreen(); // Enter fullscreen mode when starting the session
    } else {
        alert('Invalid YouTube link.');
    }
});

document.getElementById('stop-session').addEventListener('click', function() {
    stopSession();
});

function extractVideoId(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

let interval;
function startTimer() {
    let studyTime = parseInt(document.getElementById('study-time').value) * 3600;
    const timerElement = document.getElementById('timer');
    interval = setInterval(() => {
        const hours = Math.floor(studyTime / 3600);
        const minutes = Math.floor((studyTime % 3600) / 60);
        const seconds = studyTime % 60;
        timerElement.textContent = `${hours}h ${minutes}m ${seconds}s`;
        if (studyTime > 0) {
            studyTime--;
        }
        else {
            clearInterval(interval);
            alert('Study session completed!');
        }
    }, 1000);
}

function stopSession() {
    clearInterval(interval);
    document.getElementById('timer').textContent = 'Session stopped';
    document.getElementById('video-container').innerHTML = '';
    document.getElementById('stop-session').style.display = 'none';  // Hide the stop button
    exitFullscreen();
}

function enterFullscreen() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (elem.mozRequestFullScreen) { // Firefox
        elem.mozRequestFullScreen().catch(err => {
            console.log(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (elem.webkitRequestFullscreen) { // Chrome, Safari, Opera
        elem.webkitRequestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (elem.msRequestFullscreen) { // IE/Edge
        elem.msRequestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
        });
    }
}

function exitFullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen().catch(err => {
            console.log(`Error attempting to exit fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (document.mozCancelFullScreen) { // Firefox
        document.mozCancelFullScreen().catch(err => {
            console.log(`Error attempting to exit fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (document.webkitExitFullscreen) { // Chrome, Safari, Opera
        document.webkitExitFullscreen().catch(err => {
            console.log(`Error attempting to exit fullscreen mode: ${err.message} (${err.name})`);
        });
    } else if (document.msExitFullscreen) { // IE/Edge
        document.msExitFullscreen().catch(err => {
            console.log(`Error attempting to exit fullscreen mode: ${err.message} (${err.name})`);
        });
    }
}
function scrollToRegister() {
    document.getElementById("register-form").scrollIntoView({ behavior: "smooth" });
}

document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});

document.addEventListener('keydown', function(e) {
    if (e.key === "F12" || (e.ctrlKey && (e.key === 'N' || e.key === 'T' || e.key === 'W'))) {
        e.preventDefault();
    }
});

window.addEventListener('beforeunload', function(e) {
    const confirmationMessage = "Are you sure you want to leave? Your study session will be stopped.";
    e.returnValue = confirmationMessage; // Standard way to display the confirmation dialog
});

/*
function redirectToOnlyPage() {
    window.location.href = "only.html";
  }*/