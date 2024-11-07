document.addEventListener("DOMContentLoaded", function(){
    const currentPath = window.location.pathname;

    if(currentPath ==="/"){
        document.getElementById("Home-page").classList.add("active");
    }
    else if (currentPath === "/network/"){
        document.getElementById("Network-page").classList.add("active");
    }

}) 