const btnAbrirModal = document.querySelector('#btnAbrirModal');
const btnCerrarModal = document.querySelector('#btnCerrarModal');
const modal = document.querySelector('#modal');

btnAbrirModal.addEventListener('click', () => {
    modal.showModal();
});

btnCerrarModal.addEventListener('click', () => {
    modal.close();
});