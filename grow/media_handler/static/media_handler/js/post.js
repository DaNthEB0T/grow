// Chages color of saved icon o red :)
function save()
{
    icon = document.getElementById('post-save');
    num = parseInt(icon.innerHTML);

    if (icon.classList.contains('saved'))
    {
        icon.classList.remove('saved');
        var newnum = num - 1;
        document.getElementById('post-save').innerHTML = icon.innerHTML.replace("" + num, "" + newnum);
        return;
    }

    icon.classList.add('saved');
    var newnum = num + 1;
    document.getElementById('post-save').innerHTML = icon.innerHTML.replace("" + num, "" + newnum);
}
