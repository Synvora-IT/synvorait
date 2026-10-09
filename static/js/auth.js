async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const URL = "/session/login/";
    const loginBtn = document.getElementById("loginBtn");

    try {
        loginBtn.disabled = true;
        loginBtn.innerHTML = "Checking...";

        const response = await fetch(URL, {
            method: "POST",

            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({
                username: username,
                password: password,
            })
        });

        const data = await response.json();

        if (data.success === true) {
            loginBtn.innerHTML = "Success";
            loginBtn.innerHTML = "Redirecting";
            setTimeout(() => { window.location.href = "/app"; }, 1000);
        } else {
            loginBtn.disabled = false;
            loginBtn.innerHTML = "Login Failed";
        }

    } catch (error) {
        loginBtn.disabled = false;
        loginBtn.innerHTML = "Login Failed";
    }
}