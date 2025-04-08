addEventListener("DOMContentLoaded", async function () {
    const eventDropdown = document.getElementById("eventDropdown");

    try {
        const response = await fetch("http://localhost:5000/events");
        if (!response.ok) {
            throw new Error("Failed to fetch events.");
        }


        const events = await response.json();
        eventDropdown.innerHTML = '<option value="">-- Select Event --</option>';

        events.forEach(event => {
            let option = document.createElement("option");
            option.value = event.event_id;//proper event id is stored in value
            option.textContent = `Name: ${event.event_name} - City: ${event.location} Start: ${event.start_date} End: ${event.end_date}`;
            eventDropdown.appendChild(option);
        });

    } catch (error) {
        console.error("Error:", error);
        eventDropdown.innerHTML = '<option value="">Error loading events</option>';
    }
})

document.addEventListener("DOMContentLoaded", async function () {
    document.querySelector("#eventBtn").addEventListener("click", async function() {
        const eventDropdown = document.querySelector("#eventDropdown");
        const selectedEventId = eventDropdown.value; 
        
        console.log(selectedEventId);

        if (selectedEventId) {
            localStorage.setItem("eventID", selectedEventId);
    
            window.location.replace("/ticket/purchase");
        } else {
            alert("Please select an event.");
        }
    });
});