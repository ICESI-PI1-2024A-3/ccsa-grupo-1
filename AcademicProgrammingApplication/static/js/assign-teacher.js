const build_schedule = async () => {
    // Definition of start and end times
    const startHour = 7; // 7:00
    const endHour = 24; // 24:00
    // Duration of each block in minutes
    const blockDuration = 0.5; // 30 minutes
    // Get the element from the table body
    const scheduleBody = document.getElementById('schedule-body');
    // Auxiliary function to format the time
    const formatHour = (hour) => {
        if (hour % 1 === 0) {
            // If the hour is integer, show only the hour without minutes
            return hour.toString().padStart(2, '0') + ':00';
        } else {
            // If the time has a fraction, convert to HH:MM format
            const hourWithoutFraction = Math.floor(hour);
            const minutes = (hour - hourWithoutFraction) * 60;
            return hourWithoutFraction.toString().padStart(2, '0') + ':' + Math.round(minutes).toString().padStart(2, '0');
        }
    };
    // Create rows for each hour
    for (let hour = startHour; hour < endHour; hour += blockDuration) {
        const startHourFormatted = formatHour(hour);
        // Create a new row
        const row = document.createElement('tr');
        // Create cell for time
        const hourCell = document.createElement('th');
        hourCell.textContent = startHourFormatted;
        row.appendChild(hourCell);
        // Create cells for the days of the week (7 in total)
        for (let day = 0; day < 7; day++) {
            const dayCell = document.createElement('td');
            row.appendChild(dayCell);
        }
        // Add the row to the body of the table
        scheduleBody.appendChild(row);
    }
}

const get_class = async (teacher_id) => {
    try {
        const response = await fetch("./classes/${teacher_id}");
        const data = await response.json();
        if (data.message === "Success") {
            let classes = ``
        } else {
            alert("El profesor no existe.")
        }
        console.log(data);
    } catch (error) {
        console.log(error);
    }
}

const initial_charge = async () => {
    build_schedule()
    id = document.getElementById("teacher-id");
    console.log(id);
    get_class(document.getElementById("teacher-id"));
}

window.addEventListener("load", async () => {
    await initial_charge();
})