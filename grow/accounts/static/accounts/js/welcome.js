/**
 * Stop annoying transitions on window resize
 */
(function() { 
    const classes = document.body.classList;
    let timer = 0;
    window.addEventListener('resize', function () {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
        else
            classes.add('stop-transitions');

        timer = setTimeout(() => {
            classes.remove('stop-transitions');
            timer = null;
        }, 100);
    });
})();


function setActive(el) {
    // prevent clicking on both halfs at the same time
    if (document.getElementById('right-block').classList.contains("active") || document.getElementById('left-block').classList.contains("active"))
    {
        return;
    }

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
    if (document.getElementsByClassName('register-form')[0].classList.contains('active'))
    {
        document.getElementsByClassName('register-form')[0].classList.remove('active');
        return;
    }

    email = document.getElementById("register_email");
    pwd1 = document.getElementById('register_password1');
    pwd2 = document.getElementById('register_password2');

    email.style.border = "";
    pwd1.style.border = "";
    pwd2.style.border = "";

    if (email.value == "" || email.value == null)
    {
        email.style.border = "2px solid red";
        popup("Please fill in your email.", "danger");
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
        popup("Email is not valid.", "danger");
        return;
    }

    if (pwd1.value == "" || pwd1.value == null)
    {
        pwd1.style.border = "2px solid red";
        popup("Please fill in your password.", "danger");
        return;
    }
    if (pwd1.value.length < 8)
    {
        pwd1.style.border = "2px solid red";
        popup("Password must be at least 8 characters long.", "danger");
        return;
    }
    if (pwd2.value == "" || pwd2.value == null)
    {
        pwd2.style.border = "2px solid red";
        popup("Please confirm your password.", "danger");
        return;
    }
    if (pwd1.value != pwd2.value)
    {
        pwd1.style.border = "2px solid red";
        pwd2.style.border = "2px solid red";
        popup("Passwords don't match.", "danger");
        return;
    }

    document.getElementById('register-btn').disabled = false;
    document.getElementsByClassName('register-form')[0].classList.add('active');
}

/**
 * Check browser for Firefox-exclusive code
 */
if (!window.CSS.supports('-moz-transform', 'translateY(1px)'))
{
    introContent = document.getElementsByClassName('intro-content')[0];
    introContent.onscroll = function (e)
    {
        for (let i = 0; i < 3; i++)
        {
            document.getElementsByClassName('jscroll')[i].style.transform = "translateY(" + (introContent.scrollTop-document.getElementsByClassName('parallax-container')[i].offsetTop)/1.1 + "px)";
        }
    }
}
