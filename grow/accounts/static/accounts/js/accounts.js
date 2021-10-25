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