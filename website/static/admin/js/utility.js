function actionToggle() {
    var action = document.querySelector(".action");
    action.classList.toggle("active");
}

document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#date", {
        dateFormat: "d/m/Y", // Setează formatul dorit (dd/mm/yyyy)
    });
});