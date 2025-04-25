

let currentEventId = null;
let eventDetails = {};

function getEventIdFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('eventId');
}

document.addEventListener("DOMContentLoaded", () => {
  loadEventDetails();

  document.getElementById("addRaceForm").addEventListener("submit", addRace);

  document.getElementById("backBtn").addEventListener("click", () => {
    window.location.href = "/admin/operations";
  });
});


async function loadEventDetails() {
  const eventId = getEventIdFromUrl();
  if (!eventId) {
    document.getElementById("errorMessage").textContent = "No event ID provided.";
    return;
  }

  currentEventId = eventId;

  try {
    const response = await fetch(`${API_BASE_URL}/fetch/event/info?event_id=${currentEventId}`,{
            method: "GET",
            credentials: "include"
            });
    if (!response.ok) {
      throw new Error('Failed to fetch events');
    }
    const data = await response.json();

    let event;
    if (Array.isArray(data))
    {
      event = data.find(ev => ev.event_id == eventId) 
    }
    else
    {
      event = data.event_id == eventId? data : null;
    }

    
    //const event = data.find(ev => String(ev.event_id) === String(eventId));
    if (!event) {
      throw new Error('Event not found');
    }
    eventDetails = event;
    document.getElementById("eventTitle").textContent = eventDetails.event_name;
    document.getElementById("eventLocation").textContent = eventDetails.location;
    document.getElementById("eventDates").textContent =
      `${eventDetails.start_date} to ${eventDetails.end_date}`;

    loadRaces();
  } catch (error) {
    console.error('Error loading event details:', error);
    document.getElementById("errorMessage").textContent = "Failed to load event details. Please try again later.";
  }
}

async function loadRaces() {
  const racesTableBody = document.getElementById("racesTableBody");
  try {
    racesTableBody.innerHTML = `<tr><td colspan="5" class="text-center">Loading races...</td></tr>`;
    const response = await fetch(`${API_BASE_URL}/fetch/events/races?event_id=${currentEventId}`,{
      method: "GET",
      credentials: "include"
      });
    if (!response.ok) {
      throw new Error('Failed to fetch races');
    }
    const races = await response.json();

    racesTableBody.innerHTML = "";

    if (races.length === 0) {
      racesTableBody.innerHTML = `<tr><td colspan="5" class="text-center">No races found for this event.</td></tr>`;
      return;
    }

    races.forEach(race => {
      const isClosed = race.closed === 1;
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${race.race_id}</td>
        <td>${race.race_number}</td>
        <td>
          <span class="badge badge-${isClosed ? 'danger' : 'success'}">
            ${isClosed ? 'Closed' : 'Open'}
          </span>
        </td>
        <td>
          <button class="btn btn-sm btn-info btn-manage-horses" data-race-id="${race.race_id}">
            Manage Horses
          </button>
          ${!isClosed ? `<button class="btn btn-sm btn-warning btn-close-race" data-race-id="${race.race_id}">Close Betting</button>` : ''}
        </td>
      `;
      racesTableBody.appendChild(row);
    });

    document.querySelectorAll('.btn-manage-horses').forEach(btn => {
      btn.addEventListener('click', function () {
        const raceId = this.getAttribute('data-race-id');
        window.location.href = `manage-horses.html?raceId=${raceId}`; //!! missing?
      });
    });

    document.querySelectorAll('.btn-close-race').forEach(btn => {
      btn.addEventListener('click', async function () {
        const raceId = this.getAttribute('data-race-id');
        if (confirm('Are you sure you want to close this race and stop participation?')) {
          try {

            const response = await fetch(`${API_BASE_URL}/admin/races/close`, {
              method: 'PATCH',
              credentials: "include",
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ race_id: raceId })
            });
            if (!response.ok) {
              throw new Error('Failed to close race');
            }
            loadRaces();
          } catch (error) {
            console.error('Error closing race:', error);
            document.getElementById("errorMessage").textContent = "Failed to close race. Please try again later.";
          }
        }
      });
    });
  } catch (error) {
    console.error('Error loading races:', error);
    document.getElementById("errorMessage").textContent = "Failed to load races. Please try again later.";
  }
}

async function addRace(e) {
  e.preventDefault();

  const raceNumber = document.getElementById("raceNumber").value;

  try {
    const response = await fetch(`${API_BASE_URL}/admin/races/create`, {  //needs backend
      method: 'POST', 
      credentials: "include",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_id: currentEventId,
        race_number: raceNumber,
        //closed: 0
      })
    });
    if (!response.ok) {
      throw new Error('Failed to add race');
    }
    document.getElementById("addRaceForm").reset();
    document.getElementById("successMessage").textContent = "Race added successfully!";
    setTimeout(() => {
      document.getElementById("successMessage").textContent = "";
    }, 3000);
    loadRaces();
  } catch (error) {
    console.error('Error adding race:', error);
    document.getElementById("errorMessage").textContent = "Failed to add race. Please try again later.";
  }
}
