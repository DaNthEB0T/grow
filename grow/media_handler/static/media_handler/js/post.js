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
