const btn_generar_receta = document.querySelector('#btn_generar_receta');

const inputNombrePaciente = document.querySelector('#listaPacientes');
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

const modalReceta = document.querySelector('#modalReceta');

function mostarDatos() {
   console.log(`Nombre: ${inputNombrePaciente.value} Fecha: ${fecha_hora.value} Peso: ${peso.value} Edad: ${edad.value} Altura: ${altura.value} Temperatura: ${temperatura.value} Latidos: ${latidos.value} Saturacion: ${saturacion.value} Glucosa: ${glucosa.value} Sintomas: ${sintomas.value} Medicamentos: ${medicamentos.value} Indicaciones: ${indicaciones.value}`);

   console.log("nombre doctor: " + nombreDoctor.value);
   console.log("rfc doctor: " + rfc_doctor.value);
    
}


btn_generar_receta.addEventListener('click', () => {
    // verificar que no haya nulls en los inputs
    if (inputNombrePaciente.value == "" || nombreDoctor.value == "" || rfc_doctor.value == "" || fecha_hora.value == "" || peso.value == "" || edad.value == "" || altura.value == "" || temperatura.value == "" || latidos.value == "" || saturacion.value == "" || glucosa.value == "" || sintomas.value == "" || medicamentos.value == "" || indicaciones.value == "") {
        Toastify({
            text: "Complete todos los campos",
            className: "info",
            duration: 2000,
            gravity: "top",
            position: "center",
            style: {
              background: "linear-gradient(to right, #3378FF, #9442FE)",
              color: "#fff",
              fontSize: "1.2rem",
              borderRadius: "0.5rem",
              width: "50%",
              textAlign: "center",
            }
          }).showToast();
    }
    else {
        modalReceta.showModal();
    // formatear la fecha y hora
    const fecha = new Date(fecha_hora.value);
    const fecha_formateada = `${fecha.getDate()}/${fecha.getMonth() + 1}/${fecha.getFullYear()} ${fecha.getHours()}:${fecha.getMinutes()}`;

    document.querySelector('#fechaReceta').value = fecha_formateada;
    document.querySelector('#nombrePaciente').value = inputNombrePaciente.value;
    document.querySelector('#pesoPaciente').value = peso.value;
    document.querySelector('#edadPaciente').value = edad.value;
    document.querySelector('#alturaPaciente').value = altura.value;
    document.querySelector('#temperaturaPaciente').value = temperatura.value;
    document.querySelector('#lpmPaciente').value = latidos.value;
    document.querySelector('#saturacionPaciente').value = saturacion.value;
    document.querySelector('#glucosaPaciente').value = glucosa.value;

    document.querySelector('#sintomasPaciente').value = sintomas.value;
    document.querySelector('#medicamentosPaciente1').value = medicamentos.value;
    document.querySelector('#indicacionesPaciente1').value = indicaciones.value;
    }

});
const desdeaqui = document.querySelector('#desdeaqui');
const btnImprimirReceta = document.querySelector('#btnImprimirReceta');
function generarPDF() {
    html2pdf().set({
        filename: 'Receta.pdf',
    }).from(desdeaqui).save();

}

btnImprimirReceta.addEventListener('click', generarPDF);



