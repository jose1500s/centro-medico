const botonReceta = document.querySelectorAll('.receta');
const modalReceta = document.querySelector('#modalReceta');

function mostrarModalReImprimirReceta() {
    modalReceta.showModal();
    const idpaciente = this.dataset.idpaciente;
    const iddoctor = this.dataset.iddoctor;
    const fecha = this.dataset.fecha;
    const peso = this.dataset.peso;
    const altura = this.dataset.altura;
    const temperatura = this.dataset.temperatura;
    const latidos = this.dataset.latidos;
    const saturacion = this.dataset.saturacion;
    const glucosa = this.dataset.glucosa;
    const edad = this.dataset.edad;
    const sintomas = this.dataset.sintomas;
    const tratamiento = this.dataset.tratamiento;
    const indicaciones = this.dataset.indicaciones;


    document.querySelector('#fechaReceta').value = fecha
    document.querySelector('#pesoPaciente').value = peso
    document.querySelector('#edadPaciente').value = edad
    document.querySelector('#alturaPaciente').value = altura
    document.querySelector('#temperaturaPaciente').value = temperatura
    document.querySelector('#lpmPaciente').value = latidos
    document.querySelector('#saturacionPaciente').value = saturacion
    document.querySelector('#glucosaPaciente').value = glucosa
    document.querySelector('#sintomasPaciente').value = sintomas
    document.querySelector('#medicamentosPaciente1').value = tratamiento
    document.querySelector('#indicacionesPaciente1').value = indicaciones


    // document.querySelector('#sintomasPaciente').value = sintomas
   
}

// cuando se oprima el botonesEditar se ejecuta la funcion "mostrarModalEditarDoctor"
botonReceta.forEach(boton => {
    boton.addEventListener('click', mostrarModalReImprimirReceta); 
});

const desdeaqui = document.querySelector('#desdeaqui');
const btnImprimirReceta = document.querySelector('#btnImprimirReceta');
function generarPDF() {
    html2pdf().set({
        filename: 'Receta.pdf',
    }).from(desdeaqui).save();

}

btnImprimirReceta.addEventListener('click', generarPDF);