document.addEventListener("DOMContentLoaded", () => {
  const today = new Date();
  const nextWeek = new Date();
  nextWeek.setDate(today.getDate() + 7);

  const formatDate = date => date.toISOString().split('T')[0];

  document.getElementById("startDate").value = formatDate(today);
  document.getElementById("endDate").value = formatDate(nextWeek);

  document.getElementById("addEventForm").addEventListener("submit", submitEvent);

  document.getElementById("backBtn").addEventListener("click", () => {
    window.location.href = "operations.html";
  });
});

async function submitEvent(e) {
  e.preventDefault();

  const eventName = document.getElementById("eventName").value;
  const location = document.getElementById("location").value;
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const errorMessage = document.getElementById("errorMessage");
  const successMessage = document.getElementById("successMessage");

  errorMessage.textContent = "";
  successMessage.textContent = "";

  if (!eventName || !location || !startDate || !endDate) {
    errorMessage.textContent = "All fields are required.";
    return;
  }
  if (new Date(endDate) < new Date(startDate)) {
    errorMessage.textContent = "End date must be after start date.";
    return;
  }

  const eventData = {
    event_name: eventName,
    location: location,
    start_date: startDate,
    end_date: endDate
  };

  try {
    const response = await fetch('/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(eventData)
    });
    if (!response.ok) {
      throw new Error('Failed to create event');
    }
    const result = await response.json();

    successMessage.textContent = `Event "${eventName}" created successfully!`;
    document.getElementById("addEventForm").reset();

    setTimeout(() => {
      window.location.href = "operations.html";
    }, 2000);
  } catch (error) {
    console.error('Error creating event:', error);
    errorMessage.textContent = "Failed to create event. Please try again later.";
  }
}