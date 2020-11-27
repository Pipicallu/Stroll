const menuBtn = document.querySelector('.menu-btn');
let menuOpen = false;

menuBtn.addEventListener('click', () => {
    if(!menuOpen) {
        menuBtn.classList.add('open');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('open');
        menuOpen = false;
    }
});

/* nav bar display */

const navbarLinks = document.getElementsByClassName('NavBar-links')[0]
menuBtn.addEventListener('click', () =>{
    navbarLinks.classList.toggle('active');
});