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
