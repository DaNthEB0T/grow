// Chages color of saved icon o red :)
// function save()
// {
//     icon = document.getElementById('post-save');
//     num = parseInt(icon.innerHTML);

//     if (icon.classList.contains('saved'))
//     {
//         icon.classList.remove('saved');
//         var newnum = num - 1;
//         document.getElementById('post-save').innerHTML = icon.innerHTML.replace("" + num, "" + newnum);
//         return;
//     }

// VIDEO HANDLING
function pauseVid()
{
    var vid = document.getElementById("video");;
    if (vid.paused)
    {
        vid.play();
        $('.pause').get(0).innerHTML = '<i class="fas fa-pause"></i>';
    }
    else
    {
        vid.pause();
        $('.pause').get(0).innerHTML = '<i class="fas fa-play"></i>';
    }
}

function muteVid()
{
    var vid = document.getElementById("video");
    if (vid.muted)
    {
        vid.muted = false;
        $('.mute').get(0).innerHTML = '<i class="fas fa-volume-down"></i>';
    }
    else
    {
        vid.muted = true;
        $('.mute').get(0).innerHTML = '<i class="fas fa-volume-mute"></i>';
    }
}

function saveEvent(url, csrfToken, sender) { 
    var saveCount = $("#saved-count")
    var saveButton = sender
    console.log($)
    $.ajax({
        type: "POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        dataType: "json",
        success: function(response) {
            if(response.saved == true){
                // change tooltip
                $(saveButton).attr('data-bs-original-title', 'Unsave post').tooltip('show');

                saveButton.addClass("saved");
                saveCount.text(function() {
                    return $(this).text().replace($(this).text(), parseInt($(this).text()) + 1); 
                });
            }
            else if(response.saved == false){
                // change tooltip
                $(saveButton).attr('data-bs-original-title', 'Save post').tooltip('show');

                saveButton.removeClass("saved");
                saveCount.text(function() {
                    return $(this).text().replace($(this).text(), parseInt($(this).text()) - 1); 
                });
            }
        }
    });
}

function watchlistEvent(url, csrfToken, sender) { 
    console.log($)
    $.ajax({
        type: "POST",
        url: url,
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        dataType: "json",
        success: function(response) {
            selector = document.getElementsByName(response.content_id);
            if(response.added == true){

            }
            else if(response.added == false){

            }
        }
    });
}
