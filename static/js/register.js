const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector('.invalid-feedback')

usernameField.addEventListener("keyup", (e) => {

  const usernameValue = e.target.value;
  console.log("usernameValue", usernameValue);
  console.log(usernameValue.length)

  usernameField.classList.remove('is-invalid')
  feedbackArea.style.display = 'none';

  if (usernameValue.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ 'username': usernameValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if(data.username_error){
            usernameField.classList.add('is-invalid')
            feedbackArea.style.display = 'block';
            feedbackArea.innerHTML = `<p>${data.username_error}</p>`
        }
      });
  }
});
