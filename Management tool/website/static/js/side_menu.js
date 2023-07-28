// side menu
let btn = document.querySelector("#side-menu-btn");
let sidebar = document.querySelector(".side-menu");
let main = document.querySelector(".main");

btn.onclick = function() {
    btn.classList.toggle("active");
    sidebar.classList.toggle("active");
    main.classList.toggle("active");
}