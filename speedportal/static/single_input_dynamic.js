document.addEventListener('input', e => {
    submitElem = document.getElementById(e.target.parentElement.dataset.idsubmit);
    if (submitElem)
    {
        if (e.target.value.length > 0)
        {
            submitElem.removeAttribute('hidden');
        }
        else
        {
            submitElem.setAttribute('hidden', 'true');
        }
    }
});