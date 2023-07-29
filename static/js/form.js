let signup_slide = document.querySelector('#signup-btn');
let access_code_site = document.querySelector('.access_code');
let signup_site = document.querySelector('.signup_data');

signup_slide.onclick = function() {
    signup_site.style.display = 'none';
    access_code_site.style.display = 'block';
}

///Enter to submit

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    form.addEventListener('keydown', function(event) {
      if (event.keyCode === 13) { 
        event.preventDefault(); 
        form.submit();
      }
    });
  });