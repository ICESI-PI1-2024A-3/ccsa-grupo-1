const startHour = 7; // 7:00
const endHour = 24; // 24:00
const blockDuration = 0.5; // 30 minutos
const scheduleBody = document.getElementById('schedule-body');

for (let hour = startHour; hour < endHour; hour += blockDuration) {
    let startHourFormatted;
    if (hour % 1 === 0) {
        // Si la hora es entera, mostrar solo la hora sin minutos
        startHourFormatted = hour.toString().padStart(2, '0') + ':00';
    } else {
        // Si la hora tiene fracción, convertir a formato HH:MM
        const hourWithoutFraction = Math.floor(hour);
        const minutes = (hour - hourWithoutFraction) * 60;
        startHourFormatted = hourWithoutFraction.toString().padStart(2, '0') + ':' + Math.round(minutes).toString().padStart(2, '0');
    }

    const row = document.createElement('tr');
    const hourCell = document.createElement('th');
    hourCell.textContent = startHourFormatted;
    row.appendChild(hourCell);

    for (let day = 0; day < 7; day++) {
        const dayCell = document.createElement('td');
        row.appendChild(dayCell);
    }

    scheduleBody.appendChild(row);
}

// Obtener elementos del DOM
const searchBar = document.querySelector('.search-bar');
const teacherInfo = document.querySelector('.teacher-info');
const scheduleInfo = document.querySelector('.schedule-info');

// Agregar evento de clic al botón de búsqueda
document.getElementById('search-btn').addEventListener('click', function() {
    // Simular búsqueda (en este caso, siempre se muestra la información del profesor)
    const teacherFound = true;

    if (teacherFound) {
        // Mostrar información del profesor
        teacherInfo.style.display = 'block';
        scheduleInfo.style.display = 'block';
    } else {
        // Mostrar mensaje de alerta si no se encontraron resultados
        alert('No se encontraron resultados.');
    }
});