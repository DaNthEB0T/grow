// enables tooltips
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();   
});

/**
 * Displays a small dismissable popup message at top of screen
 *
function popup(m)
{
    var popup = document.createElement("DIV");
    popup.innerHTML = m + '<i class="fas fa-times" onclick="this.parentElement.remove()"></i>';
    popup.classList.add('popup');
    document.getElementsByTagName("BODY")[0].appendChild(popup);

    orderPopups();

    removePopup();
}*/

/**
 * Displays a small dismissable popup message at top of screen
 */
function popup(m, level = "white")
{
    var popup = document.createElement("DIV");
    popup.innerHTML = m + '<i class="fas fa-times" onclick="deletePopup(this.parentElement)"></i>';
    popup.classList.add('popup');
    popup.classList.add(level);
    document.getElementsByTagName("BODY")[0].appendChild(popup);

    orderPopups();

    removePopup(popup, level);
}

/**
 * Sets margin values to popups in order
 */
function orderPopups()
{
    for (i = 0; i < document.getElementsByClassName('popup').length; i++)
    {
        document.getElementsByClassName('popup')[i].style.marginTop = (3.5*i) + "rem";
    }
}

function removePopup(popup, level)
{
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
        popup.classList.add("closed");

        element = document.querySelector('.popup.closed');
        style = getComputedStyle(element);
        transition = parseFloat(style.animationDuration) * 1000;

        setTimeout(function() {
            deletePopup(popup);
        }, transition)
    }, timeOut);
}

/**
 * Fires when X is clicked on popup
 */
function deletePopup(el)
{
    el.remove();
    orderPopups();
}


/**
 * Visual effect when Save for Later button is clicked
 */
function viewLater(el)
{
    if (el.classList.contains('saved'))
    {
        return;
    }

    el.classList.add('saved');
    el.innerHTML = el.innerHTML.replace("clock", "check");
    el.innerHTML = el.innerHTML.replace("Save for later", "Saved");
}

/**
 * Opens modal window based on ID
 * @param {string} id 
 */
function modal(id)
{
    el = document.getElementById(id);
    el.style.display = "block";
}

/**
 * Closes modal widnow based on element
 * @param {element | string} el 
 */
function closeModal(el)
{
    if (typeof el === 'string' || el instanceof String)
    {
        el = document.getElementById(el);
    }
    el.style.display = "none";
}
