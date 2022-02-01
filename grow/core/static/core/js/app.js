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
function popup(m, c)
{
    if (document.getElementsByClassName("popup")[0] != null)
    {
        document.getElementsByClassName("popup")[0].remove();
    }
    var popup = document.createElement("DIV");
    popup.innerHTML = m + '<i class="fas fa-times" onclick="document.getElementsByClassName(\'popup\')[0].remove()"></i>';
    popup.classList.add('popup');
    popup.classList.add(c);
    document.getElementsByTagName("BODY")[0].appendChild(popup);

    removePopup();
}

function removePopup()
{
    setTimeout(function () {
      document.getElementsByClassName("popup")[0].remove();
    }, 7000);
}
