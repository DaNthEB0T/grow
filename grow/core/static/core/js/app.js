// enables tooltips
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();   
});

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

    removePopup();
}

/**
 * Displays a small dismissable popup message at top of screen
 */
function popup(m, level)
{
    if (document.getElementsByClassName("popup")[0] != null)
    {
        document.getElementsByClassName("popup")[0].remove();
    }
    var popup = document.createElement("DIV");
    popup.innerHTML = m + '<i class="fas fa-times" onclick="document.getElementsByClassName(\'popup\')[0].remove()"></i>';
    popup.classList.add('popup');
    popup.classList.add(level);
    document.getElementsByTagName("BODY")[0].appendChild(popup);

    removePopup(level);
}

function removePopup(level)
{
    m = document.getElementsByClassName("popup")[0];
    timeOut = -1;
    switch (level) {
        case "success":
            timeOut = 3000;
            break;
        case "secondary":
            timeOut = 4000;
            break;
        case "danger":
            break;
        case "warning":
            timeOut = 10000;
            break;
        case "info":
            timeOut = 7000;
            break;
        default:
            break;
    }
    if(timeOut < 0)
        return;
        
    setTimeout(function() { 
        m.classList.add("closed");
    }, timeOut);
}
