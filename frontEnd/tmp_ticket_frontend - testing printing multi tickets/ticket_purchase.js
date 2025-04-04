// DOM elements
const getTicketBtn = document.getElementById("getTicketBtn");
const ticketModal = document.getElementById("ticketModal");
const ticketContainer = document.getElementById("ticketContainer");
const printBtn = document.getElementById("printBtn");
const closeBtn = document.querySelector(".close");
const raceSelect = document.getElementById("raceSelect");

// Fake API response - in a real app, this would come from your backend
function fakeApiResponse(raceId) {
  return new Promise((resolve) => {
    // Simulate network delay
    setTimeout(() => {
      // Generate a random ticket ID
      const ticketId = Math.floor(Math.random() * 10000)
        .toString()
        .padStart(6, "0");

      // Get race name from the select element
      const raceName = raceSelect.options[raceSelect.selectedIndex].text;

      // Current date
      const date = new Date().toLocaleDateString();

      resolve({
        // raceDate: date,
        // ticketId: ticketId,
        // raceId: raceId,
        // horseNum: "5", 
        // eventName: "Horse Race",
        price: "$10.00",
        license: "2334556",
        event_name: 'St Patrick Fair 2022', 
        race_number: 1, 
        horse_number: 5, 
        reference_number: 41, 
        created_dttm: '2025-03-21',
      });
    }, 500); // Simulated 500ms delay
  });
}

///     HERE IS THE STUFF I ADDED     ///
// just replace what you need
// if you need more or less info just let me know and I can mess with it
// this is the milti-ticket
// Generate ticket HTML
function generateTicket(data) {
  return `
        <div class="ticket">
          <h2 align="center" id="ticketTitle">St Patrick Fair 2022</h2>
          <img align="left" class="ticketImg" id="img1" src="images/horse_scroll_1.png" alt="horse_scroll_1">
          <img align="right" class="ticketImg" id="img2" src="images/horse_scroll_1.png" alt="horse_scroll_1">
          <div>
            <li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>
          <div class="line">
            <div><li>01</li><li>05</li><li>03</li><li>00064</li></div>
            <div><li>01</li><li>05</li><li>04</li><li>00065</li></div>
            <div><li>01</li><li>05</li><li>05</li><li>00066</li></div>
            <div><li>01</li><li>05</li><li>06</li><li>00067</li></div>
            <div><li>01</li><li>05</li><li>07</li><li>00068</li></div>
            <div><li>01</li><li>05</li><li>01</li><li>00069</li></div>
            <div><li>01</li><li>05</li><li>02</li><li>00070</li></div>
            <div><li>01</li><li>05</li><li>03</li><li>00071</li></div>
            <div><li>01</li><li>05</li><li>04</li><li>00072</li></div>
            <div><li>01</li><li>05</li><li>05</li><li>00073</li></div>
          </div>
          <div><p class="textBottom">This event is sanctioned by 2334556</p></div>
        </div>

        <div class="ticket" id="ticket2">
          <h2 align="center" id="ticketTitle">St Patrick Fair 2022</h2>
          <img align="left" class="ticketImg" id="img1" src="images/horse_scroll_1.png" alt="horse_scroll_1">
          <img align="right" class="ticketImg" id="img2" src="images/horse_scroll_1.png" alt="horse_scroll_1">
          <div>
            <li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>
          <div class="line">
            <div><li>01</li><li>05</li><li>03</li><li>00064</li></div>
            <div><li>01</li><li>05</li><li>04</li><li>00065</li></div>
            <div><li>01</li><li>05</li><li>05</li><li>00066</li></div>
            <div><li>01</li><li>05</li><li>06</li><li>00067</li></div>
            <div><li>01</li><li>05</li><li>07</li><li>00068</li></div>
            <div><li>01</li><li>05</li><li>01</li><li>00069</li></div>
            <div><li>01</li><li>05</li><li>02</li><li>00070</li></div>
            <div><li>01</li><li>05</li><li>03</li><li>00071</li></div>
            <div><li>01</li><li>05</li><li>04</li><li>00072</li></div>
            <div><li>01</li><li>05</li><li>05</li><li>00073</li></div>
          </div>
          <div><p class="textBottom">This event is sanctioned by 2334556</p></div>
        </div>
    `;
}

// Event listeners
getTicketBtn.addEventListener("click", async function () {
  const raceId = raceSelect.value;

  // Show "loading" state
  getTicketBtn.disabled = true;
  getTicketBtn.textContent = "Loading...";

  try {
    // Get ticket data from API (fake in this example)
    const ticketData = await fakeApiResponse(raceId);

    // Generate and insert ticket HTML
    ticketContainer.innerHTML = generateTicket(ticketData);


    // Show the modal
    ticketModal.style.display = "block";
  } catch (error) {
    alert("Error getting ticket. Please try again.");
    console.error(error);
  } finally {
    // Reset button state
    getTicketBtn.disabled = false;
    getTicketBtn.textContent = "Get Ticket";
  }
});

// Print ticket when print button is clicked
printBtn.addEventListener("click", function () {
  // generateTicket(data);

  window.print();
});

// Close the modal when the X is clicked
closeBtn.addEventListener("click", function () {
  ticketModal.style.display = "none";
});
