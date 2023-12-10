let moderator_game_data = JSON.parse(moderators_json);

let can_make_moderators_elem = document.getElementById('can_make_moderators_id');
let can_add_categories_elem = document.getElementById('can_add_categories_id');
let can_validate_runs_elem = document.getElementById('can_validate_runs_id');
let can_ban_elem = document.getElementById('can_ban_id');
let moderator_submit_elem = document.getElementById('moderator_submit_id');

let elem_array = [ can_make_moderators_elem, can_add_categories_elem, can_validate_runs_elem, can_ban_elem ];

function set_elem_visible(elem, visible)
{
    if (visible)
    {
        elem.removeAttribute('hidden');
    }
    else
    {
        elem.setAttribute('hidden', 'true');
    }
}

function reset_elems_value()
{
    elem_array.map(function (elem) { elem.getElementsByTagName('input')[0].checked = false; });
}


document.addEventListener('change', e => {
    if (e.target.parentElement.id != 'game_choice_field_id')
    {
        return;
    }
    reset_elems_value();
    if (!e.target.value)
    {
        elem_array.map(function (elem) { set_elem_visible(elem, false); });
        set_elem_visible(moderator_submit_elem, false);
        return;
    }
    let moderator = moderator_game_data.filter(x => x.fields.game == e.target.value)[0].fields;
    console.log(moderator);
    set_elem_visible(can_make_moderators_elem, true);
    set_elem_visible(moderator_submit_elem, true);
    set_elem_visible(can_add_categories_elem, moderator.can_add_categories);
    set_elem_visible(can_validate_runs_elem, moderator.can_validate_runs);
    set_elem_visible(can_ban_elem, moderator.can_ban);
});