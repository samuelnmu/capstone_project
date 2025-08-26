function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const csrftoken = getCookie('csrftoken');

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());

        try {
            const response = await fetch("/myapp/api/users/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken   // <--- CSRF header
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert("User registered successfully!");
                window.location.href = "/myapp/login/";
            } else {
                const errorData = await response.json();
                alert("Error: " + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error("Network Error:", error);
            alert("Something went wrong! Please try again");
        }
    });
});
