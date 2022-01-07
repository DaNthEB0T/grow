function setActive(el) {
    document.getElementById(el).classList.add("active");
    document.getElementById(el).classList.remove("nonactive");
    if (el == "left-block")
    {
        document.getElementsByClassName("intro-content")[0].classList.add("active");
        document.getElementsByClassName("intro-content")[0].classList.remove("nonactive");
    }
}

function setNonActive(el, event) {
    document.getElementById(el).classList.add("nonactive");
    document.getElementById(el).classList.remove("active");
    event.stopPropagation();
    if (el == "left-block")
    {
        document.getElementsByClassName("intro-content")[0].classList.add("nonactive");
        document.getElementsByClassName("intro-content")[0].classList.remove("active");
    }
}

/**
 * Displays second part of register form
 */
function registerForm()
{
    email = document.getElementById("register_email");
    pwd1 = document.getElementById('register_password1');
    pwd2 = document.getElementById('register_password2');

    email.style.border = "";
    pwd1.style.border = "";
    pwd2.style.border = "";

    if (email.value == "" || email.value == null)
    {
        email.style.border = "2px solid red";
        popup("Please fill in your email.");
        return;
    }

    const validateEmail = (email) => {
        return String(email)
          .toLowerCase()
          .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          );
      };

    if (!validateEmail(email.value))
    {
        email.style.border = "2px solid red";
        popup("Email is not valid.");
        return;
    }

    if (pwd1.value == "" || pwd1.value == null)
    {
        pwd1.style.border = "2px solid red";
        popup("Please fill in your password.");
        return;
    }
    if (pwd2.value == "" || pwd2.value == null)
    {
        pwd2.style.border = "2px solid red";
        popup("Please confirm your password.");
        return;
    }
    if (pwd1.value != pwd2.value)
    {
        pwd1.style.border = "2px solid red";
        pwd2.style.border = "2px solid red";
        popup("Passwords don't match.");
        return;
    }
    document.getElementsByClassName('register-form')[0].classList.add('active');
}

/**
 * Displays a small dismissable popup message at top of screen
 */
function popup(m)
{
    if (document.getElementsByClassName("popup")[0] != null)
    {
        document.getElementsByClassName("popup")[0].remove();
    }
    var popup = document.createElement("DIV");
    popup.innerHTML = m + '<i class="fas fa-times" onclick="document.getElementsByClassName(\'popup\')[0].remove()"></i>';
    popup.classList.add('popup');
    document.getElementsByTagName("BODY")[0].appendChild(popup);
}
