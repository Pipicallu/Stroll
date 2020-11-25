const menuBtn = document.getElementsByClassName('.menu-btn');
let menuOpen = false;

menuBtn.addEventListener('click', () => {
    if(!menuBtn) {
        menuBtn.classList.add('open');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('open');
        menuOpen = false;
    }
});