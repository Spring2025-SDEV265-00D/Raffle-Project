

document.addEventListener("DOMContentLoaded", async function loadRaces() {
    const raceList = document.getElementById("raceDropDown");
    const ticketContent = document.getElementById("ticketContainer");
    const ticketModal = document.getElementById("ticketModal"); 
    const closeModalBtn = document.querySelector(".close"); 
    const errorMsg = document.getElementById("errorMessage");
    
    const selectedEventId = localStorage.getItem("eventID");
    console.log(selectedEventId);

    const RaceIDs = []; 
    const quantities = [];

    try {
        const response = await fetch(
            `${API_BASE_URL}/events/races?event_id=${selectedEventId}`
        );
        if (!response.ok) {
            throw new Error("Failed to fetch races.");
        }

        const races = await response.json();
        raceDropDown.innerHTML = '';

        races.forEach((race) => {
            console.log(race.race_id);
            raceDropDown.innerHTML += `<option value="${race.race_number}">${race.race_number}</option>`
        });

        raceAdd.innerHTML += `<input
        type="button"
        class="btn btn-secondary btn-lg"
        value="Add"
        id="addBtn"
        />`;

        const addBtn = document.getElementById("addBtn");

        //This code allows tickets to be added to order
        addBtn.addEventListener("click", async function () {
            const selectRace = document.getElementById(`raceDropDown`);
            const selectQuantity = document.getElementById(`quantityDropDown`);
                
                if (selectRace && selectQuantity) {
                    const selectedRace = selectRace.value; 
                    const selectedQuan = selectQuantity.value;

                    console.log(selectedRace)
                    console.log(selectedQuan)

                    const quantity = parseInt(selectedQuan);
                    const raceNum = parseInt(selectedRace);

                    if (!isNaN(quantity) && quantity > 0) {
                        quantities.push(quantity);
                        RaceIDs.push(raceNum);

                        const tableBody = document.querySelector(".table tbody");
                        const newRow = tableBody.insertRow();

                        const raceCell = newRow.insertCell(0);
                        const quantityCell = newRow.insertCell(1);

                        raceCell.textContent = raceNum;
                        quantityCell.textContent = quantity;
                    }
                    else {
                        errorMsg.innerHTML = "Must have valid quantity value.";
                        console.error(`Must have valid quantity value.`);
                    }

                } else {
                    errorMsg.innerHTML = "Could not find race.";
                    console.error(`Select element for raceId not found.`);
                }
                console.log(quantities)
                console.log(RaceIDs)
        })

        const resetBtn = document.getElementById("resetBtn");

        //This code resets table element and lists of stored values
        resetBtn.addEventListener("click", async function () {
            quantities.splice(0, quantities.length);
            RaceIDs.splice(0, RaceIDs.length);

            document.querySelector(".table tbody").innerHTML = "";
            errorMsg.innerHTML = "";
        })

        const createBtn = document.getElementById("confirmBtn");

        //This code confirms purchase with a limit of 10 tickets 
        createBtn.addEventListener("click", async function () {
           // event.preventDefault(); 
            let ticketNum = 0; 
            const ticketLim = 10;

            quantities.forEach(quantity => {
              ticketNum += quantity; 
            });

            console.log("Total Tickets: ", ticketNum);

            if (ticketNum > ticketLim) {
                console.log("Ticket limit exceeded!");
                errorMsg.innerHTML = `Ticket limit of ${ticketLim} was exceeded!`;
                quantities.splice(0, quantities.length);
                RaceIDs.splice(0, RaceIDs.length);
            }

            const ticketData = RaceIDs.map((raceId, index) => {
                return {
                    race_id: raceId,
                    qtty: quantities[index]
                };
            });

            console.log(ticketData)

            if (ticketData.length > 0) {
              const postData = { order: ticketData };

              try {
                  const thisResponse = await fetch(`${API_BASE_URL}/ticket/purchase`, {
                      method: "POST",
                      headers: {
                          "Content-Type": "application/json"
                      },
                      body: JSON.stringify(postData)
                  });

                  if (!thisResponse.ok) {
                      throw new Error("Failed to purchase tickets.");
                  }

                  const result = await thisResponse.json();
                  console.log("Ticket Purchase Response: ", result);
                  console.log("Ticket Purchase Order ID: ", result.order[0].ticket_id)
                  
                  // Generate ticket content and display the modal
                  ticketContent.innerHTML = await generateTicket(result);
                  ticketModal.style.display = "block"; // Show the modal after successful purchase
                  

              } catch (error) {
                  errorMsg.innerHTML = "Failed to post ticket purchase. Make sure horses are assigned to each race.";
                  console.error("Error posting ticket purchase: ", error);
              }
          } else {
              errorMsg.innerHTML = "No valid selections have been made.";
              console.log("No valid selections made.");
          }
      });

      closeModalBtn.addEventListener("click", () => {
         ticketModal.style.display = "none"; 
      });

  } catch (error) {
      console.error("Error:", error);
      raceList.innerHTML = '<li><div class="text-muted col-md-8 text-center text-md-start">No races are found</div></li>';
  }
});


// This function generates the ticket for displaying/printing, and can deal with up to 10 total
//* The design of this ticket is outdated, it will be updated later
async function generateTicket(data) {
    let html = '<div class="ticket">';
    html += '<h2 align="center" id="ticketTitle">' + `${data.order[0].event_name}` + '</h2>';
    html += '<img align="left" class="ticketImg" id="img1" src="../static/assets/images/horse_scroll_1.png" alt=":(">'; // alt isnt descriptive because it would 
    html += '<img align="right" class="ticketImg" id="img2" src="../static/assets/images/horse_scroll_1.png" alt="):">';// mess up the format of everything
    html += '<div>';
    html += '<li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>';
    html += '<div class="line">';

    // add all tickets into it
    //* there is a limit of 10 tickets that can be displayed
    for (let i = 0; i < data.order.length && i < 10; i++) { html += `<div><li>1</li><li>${data.order[i].race_number}</li><li>${data.order[i].horse_number}</li><li>${data.order[i].ticket_id}</li></div>`; }
    
    html += '</div>';
    html += '<div><p class="textBottom">This event is sanctioned by 2334556</p></div>';
    html += '</div>';

    
    // the second ticket is always there, but can only be seen when printing
    // the only diference is just the id in the first div
    html += '<div class="ticket" id="ticket2">';
    html += '<h2 align="center" id="ticketTitle">' + `${data.order[0].event_name}` + '</h2>';
    html += '<img align="left" class="ticketImg" id="img1" src="../static/assets/images/horse_scroll_1.png" alt=":(">';
    html += '<img align="right" class="ticketImg" id="img2" src="../static/assets/images/horse_scroll_1.png" alt="):">';
    html += '<div>';
    html += '<li>Event No.</li><li>Race No.</li><li>Horse No.</li><li>Ref No</li></div>';
    html += '<div class="line">';
    for (let i = 0; i < data.order.length && i < 10; i++) { html += `<div><li>1</li><li>${data.order[i].race_number}</li><li>${data.order[i].horse_number}</li><li>${data.order[i].ticket_id}</li></div>`; }
    html += '</div>';
    html += '<div><p class="textBottom">This event is sanctioned by 2334556</p></div>';
    html += '</div>';

  return html;
}


// Print ticket when print button is clicked
printBtn.addEventListener("click", function () {
    window.print();
  });