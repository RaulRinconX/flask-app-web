document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("popup");
    const popupDetails = document.getElementById("popup-details");
    const closePopup = document.getElementById("close-popup");
  
    closePopup.addEventListener("click", function() {
      popup.style.display = "none";
      popupDetails.innerHTML = "";
    });
  
    // Hacer una solicitud GET a la API
    fetch("http://34.160.204.45/api/historias/")
      .then(response => response.json())
      .then(data => {
        const table = document.getElementById("patient-table").getElementsByTagName('tbody')[0];
  
        data.forEach(patient => {
          const row = table.insertRow();
          const idCell = row.insertCell(0);
          const nameCell = row.insertCell(1);
          const cedulaCell = row.insertCell(2);
  
          idCell.innerHTML = patient.id;
          nameCell.innerHTML = `<a href="#" class="popup-trigger" data-patient-id="${patient.id}">${patient.nombre}</a>`;
          cedulaCell.innerHTML = patient.cedula;
        });
  
        const popupTriggers = document.querySelectorAll(".popup-trigger");
  
        popupTriggers.forEach(trigger => {
          trigger.addEventListener("click", function(event) {
            event.preventDefault();
            const patientId = this.getAttribute("data-patient-id");
  
            const patient = data.find(p => p.id == patientId);
  
            if (patient) {
              popupDetails.innerHTML = `
                <li><strong>ID:</strong> ${patient.id}</li>
                <li><strong>Nombre:</strong> ${patient.nombre}</li>
                <li><strong>Cédula:</strong> ${patient.cedula}</li>
                <li><strong>Fecha de Nacimiento:</strong> ${patient.fecha_nacimiento}</li>
                <li><strong>Tipo de Sangre:</strong> ${patient.tipo_sangre}</li>
                <li><strong>Fecha del Examen:</strong> ${patient.fecha_examen}</li>
                <li><strong>Enfermedades:</strong> ${patient.enfermedades}</li>
                <li><strong>Medicamentos:</strong> ${patient.medicamentos}</li>
                <li><strong>Alergias:</strong> ${patient.alergia}</li>
              `;
  
              popup.style.display = "block";
            }
          });
        });
      })
      .catch(error => {
        console.error("Error al obtener los datos de la API: " + error);
      });
  });