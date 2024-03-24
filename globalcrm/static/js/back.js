document.getElementById("backButton").addEventListener("click", function() {
    var currentPath = window.location.pathname;
    if (!currentPath.includes("dropdown-menu-page")) {
        window.history.back();
    } else {
        console.log("Это страница с выпадающим меню.");
    }
});