// seleccionar todos los elementos con la clase "editar" y guardarlo en una const variable llamada "botonesEditar"
const botonesEditar = document.querySelectorAll('.editar');
const btnCerrarModalMedico = document.querySelector('#btnCerrarModalMedico');
const modalEditarDoctor = document.querySelector('#modalEditarDoctor');


function mostrarModalEditarDoctor() {
    modalEditarDoctor.showModal();
    // tomar los valores que tiene el boton en el atributo data y guardarlos en una variable
    const rfc_doctor = this.dataset.rfc;
    const nombre_doctor = this.dataset.nombre;
    const cedula = this.dataset.cedula;
    const correo = this.dataset.correo;
    console.log(`rfc: ${rfc_doctor} nombre: ${nombre_doctor} cedula: ${cedula} correo: ${correo}`);

    // mandar esos valores a los inputs del modalEditarDoctor 
    document.querySelector('#rfc_editar').value = rfc_doctor;
    document.querySelector('#nombre_editar').value = nombre_doctor;
    document.querySelector('#cedula_editar').value = cedula;
    document.querySelector('#correo_editar').value = correo;
}
// cuando se oprima el botonesEditar se ejecuta la funcion "mostrarModalEditarDoctor"
botonesEditar.forEach(boton => {
    boton.addEventListener('click', mostrarModalEditarDoctor); 
});

btnCerrarModalMedico.addEventListener('click', () => {
    modalEditarDoctor.close();
});


