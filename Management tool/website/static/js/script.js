// POPUP
let signupBTN_nav = document.querySelector('#btn');
let popup = document.querySelector('.popup_container');

signupBTN_nav.onclick = function(){
  popup.classList.add('active');
}

let closePopup = document.querySelector('#close_btn');

closePopup.onclick = function(){
  popup.classList.remove('active');
}

