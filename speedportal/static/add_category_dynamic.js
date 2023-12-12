let categoryNameField = document.getElementById('category_name_field_id');
let categoryNameInput = categoryNameField.getElementsByTagName('input')[0];
let categoryModelInput = document.getElementById('category_model_field_id').getElementsByTagName('select')[0];
let categoryDescriptionInput = document.getElementById('category_description_field_id').getElementsByTagName('input')[0];
let categorySubmit = document.getElementById('category_submit_id');

document.addEventListener('change', e => {
    if (e.target != categoryModelInput)
    {
        return;
    }
    if (categoryModelInput.value == '')
    {
        categoryNameInput.value = '';
        categoryNameField.removeAttribute('hidden');
        categorySubmit.setAttribute('hidden', 'true');
    }
    else
    {
        categoryNameField.setAttribute('hidden', 'true');
        categoryNameInput.value = '1';
        if (categoryDescriptionInput.value.length > 0)
        {
            categorySubmit.removeAttribute('hidden');
        }
    }
});

document.addEventListener('input', e => {
    if (categoryNameInput.value.length == 0 || categoryDescriptionInput.value.length == 0)
    {
        categorySubmit.setAttribute('hidden', 'true');
    }
    else
    {
        categorySubmit.removeAttribute('hidden');
    }
});