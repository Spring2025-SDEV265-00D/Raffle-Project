

document.addEventListener("DOMContentLoaded", async function loadRaces() {
    const raceList = document.getElementById("raceList");
    const ticketContent = document.getElementById("ticketContainer");
    const ticketModal = document.getElementById("ticketModal"); 
    const closeModalBtn = document.querySelector(".close"); 
    
    const selectedEventId = localStorage.getItem("eventID");
    console.log(selectedEventId);

    try {
        const response = await fetch(
            `${API_BASE_URL}/events/races?event_id=${selectedEventId}`
        );
        if (!response.ok) {
            throw new Error("Failed to fetch races.");
        }

        const races = await response.json();
        raceList.innerHTML = '';

        races.forEach((race) => {
            console.log(race.race_id);
            raceList.innerHTML += `<li>
            <section>
                <div class="display-6 col-md-8 text-md-start">
                    Race - ${race.race_number}
                </div>
                <div>
                    <select class="col-md-8" id="race-${race.race_id}">
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10</option>
                    </select>
                </div>
            </section>
        </li>`
        
        });

        raceList.innerHTML += `<input
        type="button"
        class="btn btn-secondary btn-lg"
        value="Create"
        id="CreateBtn"
        />`;

        const createBtn = document.getElementById("CreateBtn");
        createBtn.addEventListener("click", async function (event) {
           // event.preventDefault(); 

            const RaceIDs = []; 
            const quantities = [];
            let ticketNum = 0; 
            const ticketLim = 10;

            races.forEach((race) => {
                const selectElement = document.getElementById(`race-${race.race_id}`);
                
                if (selectElement) {
                    const selectedValue = selectElement.value; 

                    const quantity = parseInt(selectedValue, 10);

                    if (!isNaN(quantity) && quantity > 0) {
                        quantities.push(quantity);
                        RaceIDs.push(race.race_id);
                    }

                } else {
                    console.error(`Select element for raceId ${race.race_id} not found.`);
                }
            });

            quantities.forEach(quantity => {
              ticketNum += quantity; 
            });

            console.log("Total Tickets: ", ticketNum);

            if (ticketNum > ticketLim) {
                console.log("Ticket limit exceeded!");
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
                  console.error("Error posting ticket purchase: ", error);
              }
          } else {
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