document.addEventListener('DOMContentLoaded', function() {
    const ID = window.location.pathname.slice(1);
    const spanID = document.getElementById('id-transaction');
    spanID.textContent = `${ID}`;
})