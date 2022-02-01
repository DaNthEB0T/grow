// Chages color of saved icon o red :)
function save()
{
    icon = document.getElementById('post-save');
    //num = (icon.innerHTML).replace(/(^\d+)(.+$)/i,'$1');

    if (icon.classList.contains('saved'))
    {
        icon.classList.remove('saved');
        return;
    }

    icon.classList.add('saved');
}
