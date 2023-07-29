let prevScrollPos = window.pageYOffset;
const navbar = document.querySelector('header');

window.addEventListener('scroll', () => {
  const currentScrollPos = window.pageYOffset;

  if (prevScrollPos > currentScrollPos) {
    // Scrolling up
    navbar.style.top = '0';
  } else {
    // Scrolling down
    navbar.style.top = `-${navbar.offsetHeight}px`;
  }

  prevScrollPos = currentScrollPos;
});

// REVEAL ELEMENT ON SCROLL

window.addEventListener('scroll', reveal);

function reveal() {
    var reveals = document.querySelectorAll('.reveal');

    for(var i = 0; i < reveals.length; i++) {

        var windowHeight = window.innerHeight;
        var revealTop = reveals[i].getBoundingClientRect().top;
        var revealPoint = 150;

        if (revealTop < windowHeight - revealPoint) {
            reveals[i].classList.add('revealed');
        }

        else{
            reveals[i].classList.remove('revealed');
        }
    } 
}