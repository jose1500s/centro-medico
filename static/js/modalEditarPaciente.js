const botonEditar = document.querySelectorAll('.editar');
const btnCerrarModalMedico = document.querySelector('#btnCerrarModalMedico');
const modalEditarDoctor = document.querySelector('#modalEditarDoctor');



function mostrarModalEditarPaciente() {
    modalEditarDoctor.showModal();
    // tomar los valores que tiene el boton en el atributo data y guardarlos en una variable
    const nombre_paciente = this.dataset.nombre;
    const fecha_nacimiento_paciente = this.dataset.fecha;
    const enfemedades_paciente = this.dataset.enfermedades;
    const alergias_paciente = this.dataset.alergias;
    const antecedentes_paciente = this.dataset.antecedentes;
    const id_paciente  = this.dataset.id_paciente;
    console.log(`nombre: ${nombre_paciente} fecha: ${fecha_nacimiento_paciente} enfemedades: ${enfemedades_paciente} alergias: ${alergias_paciente} antecedentes: ${antecedentes_paciente}`);

    // mandar esos valores a los inputs del modalEditarDoctor 
    document.querySelector('#nombre_editar').value = nombre_paciente
    document.querySelector('#fecha_nacimiento_nueva').value = fecha_nacimiento_paciente
    document.querySelector('#enfermedades_nuevo').value = enfemedades_paciente
    document.querySelector('#alergias_nuevo').value = alergias_paciente
    document.querySelector('#antecedentes_nuevo').value = antecedentes_paciente
    document.querySelector('#id_paciente').value = id_paciente
}
// cuando se oprima el botonesEditar se ejecuta la funcion "mostrarModalEditarDoctor"
botonEditar.forEach(boton => {
    boton.addEventListener('click', mostrarModalEditarPaciente); 
});

btnCerrarModalMedico.addEventListener('click', () => {
    modalEditarDoctor.close();
});
