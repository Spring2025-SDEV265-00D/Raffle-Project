

document.addEventListener("DOMContentLoaded", () => {
  loadEvents();

  document.getElementById("addEventBtn").addEventListener("click", () => {
/*     window.location.href = "eventAdd.html"; */
    window.location.href = "/admin/events/create";
  });
});

async function loadEvents() {
  const tableBody = document.getElementById("eventsTableBody");
  const errorMessage = document.getElementById("errorMessage");

  try {
    tableBody.innerHTML = `<tr><td colspan="6" class="text-center">Loading events...</td></tr>`;

    const response = await fetch( `${API_BASE_URL}/events`);
    if (!response.ok) {
      throw new Error('Failed to fetch events');
    }
    const events = await response.json();

    const today = new Date().toISOString().split('T')[0];

    //*commented to fetch all events (debug)
    const ongoingEvents = events//events.filter(event => event.end_date >= today);

    tableBody.innerHTML = "";

    if (ongoingEvents.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="6" class="text-center">No ongoing events found.</td></tr>`;
      return;
    }

    ongoingEvents.forEach(event => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${event.event_id}</td>
        <td>${event.event_name}</td>
        <td>${event.location}</td>
        <td>${event.start_date}</td>
        <td>${event.end_date}</td>
        <td>
          <button class="btn btn-primary btn-select" data-event-id="${event.event_id}">
            Select
          </button>
          <button class="btn btn-warning btn-manage-races" data-event-id="${event.event_id}">
            Manage Races
          </button>
        </td>
      `;
      tableBody.appendChild(row);
    });

    document.querySelectorAll('.btn-select').forEach(btn => {
      btn.addEventListener('click', function () {
        const eventId = this.getAttribute('data-event-id');
       // window.location.href = `event-details.html?eventId=${eventId}`; 
       window.location.href =  `${API_BASE_URL}/event/info?event_id=${eventId}`
      });
    });

    document.querySelectorAll('.btn-manage-races').forEach(btn => {
      btn.addEventListener('click', function () {
        const eventId = this.getAttribute('data-event-id');
        window.location.href = `/admin/event/races/manage?eventId=${eventId}`;
      });
    });
  } catch (error) {
    console.error('Error loading events:', error);
    errorMessage.textContent = "Failed to load events. Please try again later.";
  }
}
