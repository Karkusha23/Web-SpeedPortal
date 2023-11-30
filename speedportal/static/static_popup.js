let staticPopupElem;
let x_left_border;
let y_bottom_border;

document.addEventListener('mouseover', e => {
    if (staticPopupElem)
    {
        return;
    }
    let target = e.target;
    let popupHTML = target.dataset.staticpopup;
    if (!popupHTML)
    {
        return;
    }
    staticPopupElem = document.createElement('div');
    staticPopupElem.className = 'static_popup';
    staticPopupElem.innerHTML = popupHTML;
    document.body.append(staticPopupElem);

    let vec = target.getBoundingClientRect();
    let left = vec.left - staticPopupElem.offsetWidth + target.offsetWidth;
    let top = vec.top + target.offsetHeight + 5;

    staticPopupElem.style.left = left + 'px';
    staticPopupElem.style.top = top + 'px';

    x_left_border = left;
    y_bottom_border = top + staticPopupElem.offsetHeight;
});

document.addEventListener('mousemove', e => {
    if (!staticPopupElem || !x_left_border || !y_bottom_border)
    {
        return;
    }
    if (e.x < x_left_border || e.y > y_bottom_border)
    {
        hid_static_popup();
    }
});

function hid_static_popup()
{
    if (staticPopupElem)
    {
        staticPopupElem.remove();
        staticPopupElem = null;
        x_left_border = null;
        y_bottom_border = null;
    }
}
