let rejectReasonField = document.getElementById('reject_reason_p');
let submitValidation = document.getElementById('submit_validation_id');
let validationChoices = {
    'empty': '0',
    'validate' : '1',
    'reject': '2'
};

document.addEventListener('change', e => {
    switch (e.target.value)
    {
    case validationChoices['empty']:
        rejectReasonField.setAttribute('hidden', 'true');
        submitValidation.setAttribute('hidden', 'true');
        break;
    case validationChoices['validate']:
        rejectReasonField.setAttribute('hidden', 'true');
        rejectReasonField.value = '1';
        submitValidation.removeAttribute('hidden');
        break;
    case validationChoices['reject']:
        rejectReasonField.removeAttribute('hidden');
        rejectReasonField.value = null;
        submitValidation.removeAttribute('hidden');
    }
});