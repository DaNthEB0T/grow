div = document.getElementsByClassName('content')[0];
thing = document.getElementById('thing');
bg = document.getElementsByClassName('content-container')[0];

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

/**
 * Visually removes post from list (with animation)
 */
function removePost(el)
{
    el = el.parentElement;
    el.classList.add('removed');

    setTimeout(function () {
        container = document.getElementsByClassName('post-tiles-container')[0];
    
        var postSlide = document.createElement('div');
        postSlide.classList.add('post-slide');
        postSlide.innerHTML = "<div></div>";
    
        container.insertBefore(postSlide, el);
        el.remove();
    
        setTimeout(function () {
            postSlide.remove();
        }, 500);
    }, 500);
}
