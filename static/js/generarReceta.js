const btnGenerarReceta = document.querySelector('#probando');

const inputNombrePaciente = document.querySelector('#nombre_paciente');
const nombreDoctor = document.querySelector('#nombre_doctor');
const rfc_doctor = document.querySelector('#rfc_doctor');
const fecha_hora = document.querySelector('#fecha_hora');
const peso = document.querySelector('#peso');
const edad = document.querySelector('#edad');
const altura = document.querySelector('#altura');
const temperatura = document.querySelector('#temperatura');
const latidos = document.querySelector('#latidos');
const saturacion = document.querySelector('#saturacion');
const glucosa = document.querySelector('#glucosa');
const sintomas = document.querySelector('#sintomas');
const medicamentos = document.querySelector('#medicamentos');
const indicaciones = document.querySelector('#indicaciones');


function mostarDatos() {
   console.log(`Nombre: ${inputNombrePaciente.value} Fecha: ${fecha_hora.value} Peso: ${peso.value} Edad: ${edad.value} Altura: ${altura.value} Temperatura: ${temperatura.value} Latidos: ${latidos.value} Saturacion: ${saturacion.value} Glucosa: ${glucosa.value} Sintomas: ${sintomas.value} Medicamentos: ${medicamentos.value} Indicaciones: ${indicaciones.value}`);

   console.log("nombre doctor: " + nombreDoctor.value);
   console.log("rfc doctor: " + rfc_doctor.value);
    
}

btnGenerarReceta.addEventListener('click', () => {
    mostarDatos();
   
});