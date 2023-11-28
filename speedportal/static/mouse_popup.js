let mousePopupElem;

document.addEventListener('mousemove', event => {
    if (!mousePopupElem || !event.target)
    {
        return;
    }
    let x = event.x + 10;
    let y = event.y + 10;
    mousePopupElem.style.left = x + 'px';
    mousePopupElem.style.top = y + 'px';
});

function show_mouse_popup(text)
{
    hid_mouse_popup();
    mousePopupElem = document.createElement('div');
    mousePopupElem.className = 'mouse_popup';
    mousePopupElem.innerHTML = text;
    document.body.append(mousePopupElem);
}

function hid_mouse_popup()
{
    if (mousePopupElem)
    {
        mousePopupElem.remove();
        mousePopupElem = null;
    }
}
