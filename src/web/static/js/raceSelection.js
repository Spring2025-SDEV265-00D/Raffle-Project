const { API_BASE_URL } = window.ENV;

document.addEventListener("DOMContentLoaded", async function loadRaces() {
  const raceList = document.getElementById("raceDropDown");
  const raceAdd = document.getElementById("raceAdd");
  const ticketContent = document.getElementById("ticketContainer");
  const ticketModal = document.getElementById("ticketModal");
  const closeModalBtn = document.getElementById("closeModal");
  const errorMsg = document.getElementById("errorMessage");
  const printBtn = document.getElementById("printBtn");

  // Add print button event listener if it exists
  if (printBtn) {
    printBtn.addEventListener("click", function () {
      window.print();
    });
  }

  // Add close modal button event listener if it exists
  if (closeModalBtn && ticketModal) {
    closeModalBtn.addEventListener("click", () => {
      ticketModal.style.display = "none";
    });
  }

  const selectedEventId = localStorage.getItem("eventID");
  if (!selectedEventId) {
    errorMsg.innerHTML = "No event selected. Please select an event first.";
    return;
  }
  console.log("Selected Event ID:", selectedEventId);

  const RaceIDs = [];
  const quantities = [];

  try {
    const response = await fetch(
      `${API_BASE_URL}/fetch/events/races?event_id=${selectedEventId}`,
      {
        method: "GET",
        credentials: "include",
      }
    );

    if (!response.ok) {
      throw new Error("Failed to fetch races.");
    }

    const races = await response.json();
    console.log("Fetched races:", races);

    if (!raceList) {
      throw new Error("Race dropdown element not found");
    }

    // Clear existing options
    raceList.innerHTML = "";

    // Add default option
    raceList.innerHTML = '<option value="">Select a Race</option>';

    // Add race options
    races.forEach((race) => {
      console.log("Processing race:", race);
      if (race.closed === 0) {
        const option = document.createElement("option");
        option.value = race.race_number;
        option.textContent = `Race ${race.race_number}`;
        raceList.appendChild(option);
      }
    });

    if (!raceAdd) {
      throw new Error("Race add element not found");
    }

    // Add the Add button if it doesn't exist
    if (!document.getElementById("addBtn")) {
      raceAdd.innerHTML = `<input
        type="button"
        class="btn btn-secondary btn-lg"
        value="Add"
        id="addBtn"
      />`;
    }

    const addBtn = document.getElementById("addBtn");
    if (!addBtn) {
      throw new Error("Add button not found");
    }

    //This code allows tickets to be added to order
    addBtn.addEventListener("click", async function () {
      const selectRace = document.getElementById("raceDropDown");
      const selectQuantity = document.getElementById("quantityDropDown");

      if (selectRace && selectQuantity) {
        const selectedRace = selectRace.value;
        const selectedQuan = selectQuantity.value;

        console.log("Selected Race:", selectedRace);
        console.log("Selected Quantity:", selectedQuan);

        const quantity = parseInt(selectedQuan);
        const raceNum = parseInt(selectedRace);

        if (!isNaN(quantity) && quantity > 0 && !isNaN(raceNum) && raceNum > 0) {
          quantities.push(quantity);
          RaceIDs.push(raceNum);

          // Get the table and ensure it has a tbody
          const table = document.querySelector("table");
          if (!table) {
            throw new Error("Table not found");
          }

          let tableBody = table.querySelector("tbody");
          if (!tableBody) {
            tableBody = document.createElement("tbody");
            table.appendChild(tableBody);
          }

          const newRow = tableBody.insertRow();
          const raceCell = newRow.insertCell(0);
          const quantityCell = newRow.insertCell(1);

          raceCell.textContent = raceNum;
          quantityCell.textContent = quantity;
        } else {
          errorMsg.innerHTML = "Must have valid race and quantity values.";
          console.error("Invalid race or quantity values");
        }
      } else {
        errorMsg.innerHTML = "Could not find race or quantity selection.";
        console.error("Select elements not found");
      }
      console.log("Current quantities:", quantities);
      console.log("Current RaceIDs:", RaceIDs);
    });

    const resetBtn = document.getElementById("resetBtn");
    if (resetBtn) {
      //This code resets table element and lists of stored values
      resetBtn.addEventListener("click", async function () {
        quantities.splice(0, quantities.length);
        RaceIDs.splice(0, RaceIDs.length);

        const table = document.querySelector("table");
        if (table) {
          const tableBody = table.querySelector("tbody");
          if (tableBody) {
            tableBody.innerHTML = "";
          }
        }
        errorMsg.innerHTML = "";
      });
    }

    const createBtn = document.getElementById("confirmBtn");
    if (createBtn) {
      //This code confirms purchase with a limit of 10 tickets
      createBtn.addEventListener("click", async function () {
        let ticketNum = 0;
        const ticketLim = 10;

        quantities.forEach((quantity) => {
          ticketNum += quantity;
        });

        console.log("Total Tickets:", ticketNum);

        if (ticketNum > ticketLim) {
          console.log("Ticket limit exceeded!");
          errorMsg.innerHTML = `Ticket limit of ${ticketLim} was exceeded!`;
          quantities.splice(0, quantities.length);
          RaceIDs.splice(0, RaceIDs.length);
          return;
        }

        const ticketData = RaceIDs.map((raceId, index) => {
          return {
            race_id: raceId,
            qtty: quantities[index],
          };
        });

        console.log("Ticket data to send:", ticketData);

        if (ticketData.length > 0) {
          const postData = { order: ticketData };

          try {
            const thisResponse = await fetch(
              `${API_BASE_URL}/pos/ticket/purchase`,
              {
                method: "POST",
                credentials: "include",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(postData),
              }
            );

            if (!thisResponse.ok) {
              throw new Error("Failed to purchase tickets.");
            }

            const result = await thisResponse.json();
            console.log("Ticket Purchase Response:", result);
            console.log("Ticket Purchase Order ID:", result.order[0].ticket_id);

            // Generate ticket content and display the modal
            if (ticketContent && ticketModal) {
              ticketContent.innerHTML = await generateTicket(result);
              ticketModal.style.display = "block"; // Show the modal after successful purchase
            }
          } catch (error) {
            errorMsg.innerHTML =
              "Failed to post ticket purchase. Make sure horses are assigned to each race.";
            console.error("Error posting ticket purchase:", error);
          }
        } else {
          errorMsg.innerHTML = "No valid selections have been made.";
          console.log("No valid selections made.");
        }
      });
    }
  } catch (error) {
    console.error("Error loading races:", error);
    if (raceList) {
      raceList.innerHTML =
        '<option value="">Error loading races</option>';
    }
    errorMsg.innerHTML = "Failed to load races. Please try again later.";
  }
});

// This function generates the ticket for displaying/printing, and can deal with up to 10 total
//* The design of this ticket is outdated, it will be updated later
async function generateTicket(data) {
  let html = '<div class="ticket">';
  html +=
    '<h2 align="center" id="ticketTitle">' +
    `${data.order[0].event_name}` +
    "</h2>";
  html +=
    '<img align="left" class="ticketImg" id="img1" src="../static/assets/images/horse_scroll_final.png" alt=":(">'; // alt isnt descriptive because it would
  html +=
    '<img align="right" class="ticketImg" id="img2" src="../static/assets/images/horse_scroll_final.png" alt="):">'; // mess up the format of everything
  html += "<div>";
  html +=
    "<li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>";
  html += '<div class="line">';

  // add all tickets into it
  //* there is a limit of 10 tickets that can be displayed
  for (let i = 0; i < data.order.length && i < 10; i++) {
    html += `<div><li>1</li><li>${data.order[i].race_number}</li><li>${data.order[i].horse_number}</li><li>${data.order[i].ticket_id}</li></div>`;
  }

  html += "</div>";
  html +=
    '<div><p class="textBottom">This event is sanctioned by 2334556</p></div>';
  html += "</div>";

  // the second ticket is always there, but can only be seen when printing
  // the only diference is just the id in the first div
  html += '<div class="ticket" id="ticket2">';
  html +=
    '<h2 align="center" id="ticketTitle">' +
    `${data.order[0].event_name}` +
    "</h2>";
  html +=
    '<img align="left" class="ticketImg" id="img1" src="../static/assets/images/horse_scroll_final.png" alt=":(">';
  html +=
    '<img align="right" class="ticketImg" id="img2" src="../static/assets/images/horse_scroll_final.png" alt="):">';
  html += "<div>";
  html +=
    "<li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>";
  html += '<div class="line">';
  for (let i = 0; i < data.order.length && i < 10; i++) {
    html += `<div><li>1</li><li>${data.order[i].race_number}</li><li>${data.order[i].horse_number}</li><li>${data.order[i].ticket_id}</li></div>`;
  }
  html += "</div>";
  html +=
    '<div><p class="textBottom">This event is sanctioned by 2334556</p></div>';
  html += "</div>";

  return html;
}

// Print ticket when print button is clicked
printBtn.addEventListener("click", function () {
  window.print();
});
