function show_text(show_id, hid_id)
{
    document.getElementById(show_id).removeAttribute('hidden');
    document.getElementById(hid_id).setAttribute('hidden', 'true');
}
