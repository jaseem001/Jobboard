document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit',function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Loading.......
                `;
                submitButton.disabled = true;
            }
        });
    });

const fileInputs = document.querySelectorAll('input[type="file"]');
fileInputs.forEach(input => {
    input.addEventListener('change', function(){
        const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
        const label = this.nextElementSibling;
        if (label && label.tagName == 'LABEL') {
            label.textContent = fileName;
        }

     });
   });
document.querySelectorAll('.apply-now').forEach(button => {
    button.addEventListener('click', function() {
        alert('You are applying for this job.')
    });
});

});

