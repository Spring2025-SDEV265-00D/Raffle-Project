document.addEventListener("DOMContentLoaded", async function loadRaces() {
    const raceList = document.getElementById("raceList");
    const ticketContent = document.getElementById("ticketContainer");
    const ticketModal = document.getElementById("ticketModal"); 
    const closeModalBtn = document.querySelector(".close"); 
    
    const selectedEventId = localStorage.getItem("eventID");
    console.log(selectedEventId);

    try {
        const response = await fetch(
            `http://localhost:5000/events/races?event_id=${selectedEventId}`
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
                  const thisResponse = await fetch("http://localhost:5000/ticket/purchase", {
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

async function generateTicket(data) {
  let html = '';

  for (let i = 0; i < data.order.length; i++) {
    html += `
        <div class="ticket-content">
            <p><strong>Ticket ID:</strong> ${data.order[i].ticket_id}</p>
            <p><strong>Event:</strong> ${data.order[i].event_name}</p>
            <p><strong>Bought:</strong> ${data.order[i].created_dttm}</p>
            <p><strong>Race Number:</strong> ${data.order[i].race_number}</p>
            <p><strong>Horse Number:</strong> ${data.order[i].horse_number}</p>
        </div>
  `;
  }

  return html;
}