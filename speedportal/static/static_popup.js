let staticPopupElem;

document.addEventListener('mouseover', e => {
    if (staticPopupElem)
    {
        return;
    }
    let target = e.target;
    let popupHTML = target.dataset.popup;
    if (!popupHTML)
    {
        return;
    }
    staticPopupElem = document.createElement('div');
    staticPopupElem.setAttribute('onmouseout', 'hid_static_popup()');
    staticPopupElem.className = 'static_popup';
    staticPopupElem.innerHTML = popupHTML;
    document.body.append(staticPopupElem);

    let vec = target.getBoundingClientRect();
    let left = vec.left;
    let top = vec.top + staticPopupElem.offsetHeight;

    console.log(vec.left);
    staticPopupElem.style.left = left + 'px';
    staticPopupElem.style.top = top + 'px';
});

function hid_static_popup()
{
    if (staticPopupElem)
    {
        staticPopupElem.remove();
        staticPopupElem = null;
    }
}
