div = document.getElementsByClassName('content')[0];
thing = document.getElementsByClassName('head-tile')[0];
bg = document.getElementsByClassName('inner-content-container')[0];

div.onscroll = calcBg;


// Moves background horizontally when scrolling
function calcBg()
{
    var rect = thing.getBoundingClientRect();
    y = rect.top;

    width = bg.offsetWidth;

    bg.style.backgroundPosition = (0 - y) + "px center";
}

calcBg();
