// 4/18/25 - Entering a valid reference number and clicking either of the buttons will collect 
// the ticket information for that reference number. Clicking Redeem or Refund will display the 
// correct response to the cashier. Would maybe like this to be in a pop up window or have a way
// to clear it.

document.addEventListener("DOMContentLoaded", async function () {
    document.querySelector("#redeemBtn").addEventListener("click", async function() {
        const referenceNum = document.querySelector("#referenceNum");
        const numResult = document.getElementById("result");
        
        console.log(referenceNum.value)

        try {
            const response = await fetch(`http://localhost:5000/ticket/info?ticket_id=${referenceNum.value}`);
            if (response.ok) {
                const ticketData = await response.json();
    
                console.log(ticketData.ticket_id)

                //NOTE this is for cases where the "Redeem" button is clicked.
                //TO DO: add a way to clear the message that is displayed, maybe add message to pop up window.

                try {
                    const thisResponse = await fetch("http://localhost:5000/ticket/update", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            ticket_id: ticketData.ticket_id,
                            request: "redeem"
                        })
                    });
  
                    if (!thisResponse.ok) {
                        const result = await thisResponse.json();
                        console.log("JSON response: ", result);

                        numResult.innerHTML = '';

                        const getResponse = result.split("}");

                        const responseStr = "Ticket" + getResponse[1]

                        numResult.innerHTML = `<h1 class="display-6 row justify-content-center">${responseStr}</h1>`
                        throw new Error("Failed to redeem ticket.");

                    }
                    else {
                        numResult.innerHTML = `<h1 class="display-6 row justify-content-center">Congrats! Ticket is a Winner!</h1>`
                    }
  
                } catch (error) {
                    console.error("Error with redeem button: ", error);
                }

            }
            else {
                throw new Error("Failed to fetch ticket information.");
            }
    
    
        } catch (error) {
            console.error("Error:", error);
        }
    })

    document.querySelector("#refundBtn").addEventListener("click", async function() {
        const referenceNum = document.querySelector("#referenceNum");
        const numResult = document.getElementById("result");
        console.log(referenceNum.value)

        try {
            const response = await fetch(`http://localhost:5000/ticket/info?ticket_id=${referenceNum.value}`);
            if (response.ok) {
                const ticketData = await response.json();
    
                console.log(ticketData.ticket_id)

                //NOTE this is for cases where the "Refund" button is clicked.
                
                try {
                    const thisResponse = await fetch("http://localhost:5000/ticket/update", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            ticket_id: ticketData.ticket_id,
                            request: "refund"
                        })
                    });
  
                    if (!thisResponse.ok) {
                        const result = await thisResponse.json();
                        console.log("JSON response: ", result);

                        numResult.innerHTML = '';

                        const getResponse = result.split("}");

                        const responseStr = "Ticket" + getResponse[1]

                        numResult.innerHTML = `<h1 class="display-6 row justify-content-center">${responseStr}</h1>`
                        throw new Error("Failed to refund ticket.");

                    }
                    else {
                        numResult.innerHTML = `<h1 class="display-6 row justify-content-center">Ticket Receives Full Refund.</h1>`
                    }
  
                } catch (error) {
                    console.error("Error with redeem button: ", error);
                }

            }
            else {
                throw new Error("Failed to fetch ticket information.");
            }
    
    
        } catch (error) {
            console.error("Error:", error);
        }
    })
})