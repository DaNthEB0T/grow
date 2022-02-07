var imgInput = document.getElementById("id_thumbnail");
var titleInput = document.getElementById("id_title");
var prevImg = document.getElementById("preview-img");
var prevTitle = document.getElementById("preview-title");

imgInput.onchange = updateImage;

$(titleInput).on("change keyup paste", updateTitle);

/**
 * Updates image in preview
 */
function updateImage()
{
    const [file] = imgInput.files;
    if (file) {
        prevImg.src = URL.createObjectURL(file);
    }
}

/**
 * Updates image in preview
 */
function updateTitle() {
    prevTitle.innerHTML = titleInput.value;
}


if (titleInput.value)
{
    updateTitle();
}
updateImage();

/**
 * Script for making nice tags
 */
var tagInput = document.getElementById("tag-input");
var actualTagInput = document.getElementById("id_tags");
// clear acttual invisible input on page load just in case
actualTagInput.value = "";

$(tagInput).on("change keyup paste", updateTags);

function updateTags()
{
    //set width of input to match inner text
    var widthCalc = document.createElement('span');
    document.getElementsByTagName("BODY")[0].appendChild(widthCalc);
    widthCalc.classList.add('width-calc');
    widthCalc.innerHTML = tagInput.value;
    var width = widthCalc.getBoundingClientRect().width;
    widthCalc.remove();
    tagInput.style.width = "calc(1rem + " + width + "px)";

    // split text into tags
    if (tagInput.value.includes(' '))
    {
        // remove unwanted characters form input
        tagInput.value = tagInput.value.replace(/[^\w\-\ ]/gi, '');

        // split the string
        var split = tagInput.value.split(' ');

        // check for duplicate tags
        var duplicate = false;
        for (tag of document.getElementsByClassName('input-tag'))
        {
            if (tag.innerText.replace(/ /g, "") == split[0])
            {
                duplicate = true;
                break;
            }
        }

        // tagify first element of array
        if (split[0])
        {
            // add the tag element
            if (!duplicate)
            {
                var newtag = document.createElement('span');
                newtag.classList.add('input-tag');
                newtag.innerHTML = split[0].toLowerCase() + ' <i class="fas fa-times" onclick="removeTag(this.parentElement)"></i>';
                document.getElementById('tags').appendChild(newtag);
            }
            
            // delete tagified text from input
            tagInput.value = tagInput.value.replace(split[0], "");
        }

        // delete all spaces in input
        tagInput.value = tagInput.value.replace(/ /g, "");
    }

    // update actual input according to existing tags and tag input
    updateTagInput();
}

function updateTagInput()
{
    var tagList = document.getElementsByClassName('input-tag');
    actualTagInput.value = "";
    for (i = 0; i < tagList.length; i++)
    {
        actualTagInput.value = actualTagInput.value + tagList[i].innerText + ",";
    }
    actualTagInput.value = actualTagInput.value + tagInput.value.toLowerCase().replace(/[^\w\-]/gi, '');
}

function removeTag(el)
{
    el.remove();
    updateTagInput();
}
