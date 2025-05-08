const { API_BASE_URL } = window.ENV;

const urlParams = new URLSearchParams(window.location.search);
const raceId = urlParams.get('raceId');
const eventId = urlParams.get('eventId');

const errorMessageEl = document.getElementById('errorMessage');
const successMessageEl = document.getElementById('successMessage');
const eventNameEl = document.getElementById('eventName');
const eventLocationEl = document.getElementById('eventLocation');
const raceNameEl = document.getElementById('raceName');
const raceStatusEl = document.getElementById('raceStatus');
const horsesTableBodyEl = document.getElementById('horsesTableBody');
const addHorseFormEl = document.getElementById('addHorseForm');
const backBtnEl = document.getElementById('backBtn');

const confirmActionModalEl = document.getElementById('confirmActionModal');
const confirmActionModalBodyEl = document.getElementById('confirmActionModalBody');
const confirmActionBtnEl = document.getElementById('confirmActionBtn');
const cancelActionBtnEl = document.getElementById('cancelActionBtn');

let currentAction = {
  type: null,
  horseId: null,
};

document.addEventListener('DOMContentLoaded', async () => {
  if (!raceId) {
    showError('Race ID is required');
    return;
  }

  try {
    const race = await fetchRaceDetails(raceId);
    const currentEventId = eventId || race.event_id;
    
    await loadRaceAndEventDetails(race, currentEventId);
    
    await loadHorses();
    
    setupEventListeners(currentEventId);
  } catch (error) {
    console.error('Error initializing page:', error);
    showError('Failed to initialize page. Please try again later.');
  }
});

function setupEventListeners(currentEventId) {
  addHorseFormEl.addEventListener('submit', async (e) => {
    e.preventDefault();
    await addHorse();
  });

  backBtnEl.addEventListener('click', () => {
    window.location.href = `/admin/event/races/manage?eventId=${currentEventId}`;
  });

  confirmActionBtnEl.addEventListener('click', async () => {
    hideModal();

    if (currentAction.type === 'scratched') {
      await updateHorse(currentAction.horseId, 'scratched');
    } else if (currentAction.type === 'winner') {
      await updateHorse(currentAction.horseId, 'winner');
    }

    currentAction = { type: null, horseId: null };
  });
  
  cancelActionBtnEl.addEventListener('click', () => {
    hideModal();
    currentAction = { type: null, horseId: null };
  });
}

async function fetchRaceDetails(raceId) {
  try {
    const response = await fetch(`${API_BASE_URL}/fetch/race/info?race_id=${raceId}`, {
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch race details');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching race:', error);
    throw new Error('Failed to get race information');
  }
}

async function loadRaceAndEventDetails(race, eventId) {
  try {
    const eventResponse = await fetch(`${API_BASE_URL}/fetch/event/info?event_id=${eventId}`, {
      credentials: 'include'
    });
    
    if (!eventResponse.ok) {
      throw new Error('Failed to fetch event details');
    }
    
    const eventData = await eventResponse.json();
    const event = Array.isArray(eventData) ? eventData.find(e => e.event_id == eventId) : eventData;
    
    if (!event) {
      throw new Error('Event not found');
    }

    updateRaceAndEventDetails(race, event);
  } catch (error) {
    console.error('Error loading event details:', error);
    showError('Failed to load event details');
  }
}

function updateRaceAndEventDetails(race, event) {
  eventNameEl.textContent = event.event_name;
  eventLocationEl.textContent = event.location;

  raceNameEl.textContent = `Race #${race.race_number}`;
  
  const isClosed = race.closed === 1;
  raceStatusEl.textContent = isClosed ? 'Closed' : 'Open';
  
  raceStatusEl.className = 'px-2 py-1 rounded text-white';
  raceStatusEl.classList.add(isClosed ? 'bg-red-600' : 'bg-green-600');
}

async function loadHorses() {
  try {
    const response = await fetch(`${API_BASE_URL}/fetch/races/horses?race_id=${raceId}`, {
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch horses');
    }
    
    const horses = await response.json();
    
    updateHorsesTable(horses);
  } catch (error) {
    console.error('Error loading horses:', error);
    showError('Failed to load horses for this race');
  }
}

function updateHorsesTable(horses) {
  horsesTableBodyEl.innerHTML = '';
  
  if (horses.length === 0) {
    const noHorsesRow = document.createElement('tr');
    noHorsesRow.innerHTML = `
      <td colspan="3" class="text-center py-4">No horses added to this race yet</td>
    `;
    horsesTableBodyEl.appendChild(noHorsesRow);
    return;
  }
  
  horses.forEach(horse => {
    const row = document.createElement('tr');
    
    let statusLabel = 'Active';
    let statusClass = 'bg-blue-600';
    
    if (horse.scratched === 1) {
      statusLabel = 'Scratched';
      statusClass = 'bg-gray-600';
      row.classList.add('bg-gray-100');
    } else if (horse.winner === 1) {
      statusLabel = 'Winner';
      statusClass = 'bg-green-600';
      row.classList.add('bg-green-50');
    }
    
    let actionButtons = '';
    
    const canAct = horse.scratched !== 1 && horse.winner !== 1;
    
    if (canAct) {
      actionButtons = `
        <button class="btn-scratch py-1 px-3 bg-yellow-500 hover:bg-yellow-600 text-white rounded mr-2" 
                data-horse-id="${horse.horse_id}">Scratch</button>
        <button class="btn-winner py-1 px-3 bg-green-500 hover:bg-green-600 text-white rounded" 
                data-horse-id="${horse.horse_id}">Set Winner</button>
      `;
    }
    
    row.innerHTML = `
      <td class="py-2 px-4 border-b">${horse.horse_number}</td>
      <td class="py-2 px-4 border-b">
        <span class="px-2 py-1 text-white rounded ${statusClass}">${statusLabel}</span>
      </td>
      <td class="py-2 px-4 border-b">${actionButtons}</td>
    `;
    
    horsesTableBodyEl.appendChild(row);
  });
  
  document.querySelectorAll('.btn-scratch').forEach(btn => {
    btn.addEventListener('click', () => confirmAction('scratched', btn.dataset.horseId));
  });
  
  document.querySelectorAll('.btn-winner').forEach(btn => {
    btn.addEventListener('click', () => confirmAction('winner', btn.dataset.horseId));
  });
}

async function addHorse() {
  const horseNumber = document.getElementById('horseNumber').value;
  
  clearMessages();
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/races/horses/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        horse_number: parseInt(horseNumber, 10),
        race_id: parseInt(raceId, 10)
      }),
      credentials: 'include'
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to add horse');
    }
    
    showSuccess('Horse added successfully');
    
    addHorseFormEl.reset();
    
    await loadHorses();
  } catch (error) {
    console.error('Error adding horse:', error);
    showError(error.message || 'Failed to add horse');
  }
}

function confirmAction(action, horseId) {
  currentAction = {
    type: action,
    horseId: horseId
  };
  
  let message = '';
  if (action === 'scratched') {
    message = 'Are you sure you want to mark this horse as scratched? This action cannot be undone.';
  } else if (action === 'winner') {
    message = 'Are you sure you want to set this horse as the winner? This action cannot be undone.';
  }
  
  confirmActionModalBodyEl.textContent = message;
  
  showModal();
}

async function updateHorse(horseId, action) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/races/update`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        horse_id: parseInt(horseId, 10),
        request: action
      }),
      credentials: 'include'
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `Failed to update horse status to ${action}`);
    }
    
    showSuccess(`Horse ${action === 'winner' ? 'set as winner' : 'scratched'} successfully`);
    
    await loadHorses();
  } catch (error) {
    console.error(`Error updating horse to ${action}:`, error);
    showError(error.message || `Failed to update horse status`);
  }
}

function showModal() {
  confirmActionModalEl.classList.remove('hidden');
}

function hideModal() {
  confirmActionModalEl.classList.add('hidden');
}

function showError(message) {
  errorMessageEl.textContent = message;
  errorMessageEl.style.display = 'block';
  successMessageEl.style.display = 'none';
}

function showSuccess(message) {
  successMessageEl.textContent = message;
  successMessageEl.style.display = 'block';
  errorMessageEl.style.display = 'none';
}

function clearMessages() {
  errorMessageEl.style.display = 'none';
  successMessageEl.style.display = 'none';
}