function setActive(el) {
    document.getElementById(el).classList.add("active");
    if (el == "left-block")
    {
        document.getElementsByClassName("intro-content")[0].classList.add("active");
    }
}