// 4/11/25 - Entering a valid reference number and clicking either of the buttons will collect 
// the ticket information for that reference number, but the ticket/update route still needs to
// be utilized as mentioned in the comments.

document.addEventListener("DOMContentLoaded", async function () {
    document.querySelector("#redeemBtn").addEventListener("click", async function() {
        const referenceNum = document.querySelector("#referenceNum");
        console.log(referenceNum.value)

        try {
            const response = await fetch(`http://localhost:5000/ticket/info?ticket_id=${referenceNum.value}`);
            if (response.ok) {
                const ticketData = await response.json();
    
                console.log(ticketData.ticket_id)

                //NOTE this is for cases where the "Redeem" button is clicked.
                //TO DO: use ticket/update route to post data in this format: {"ticket_id": ticketData.ticket_id, "request": "redeem"}.
                //take response from that route and display it to the user in some way.

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
        console.log(referenceNum.value)

        try {
            const response = await fetch(`http://localhost:5000/ticket/info?ticket_id=${referenceNum.value}`);
            if (response.ok) {
                const ticketData = await response.json();
    
                console.log(ticketData.ticket_id)

                //NOTE this is for cases where the "Refund" button is clicked.
                //TO DO: use ticket/update route to post data in this format: {"ticket_id": ticketData.ticket_id, "request": "refund"}.
                //take response from that route and display it to the user in some way.

            }
            else {
                throw new Error("Failed to fetch ticket information.");
            }
    
    
        } catch (error) {
            console.error("Error:", error);
        }
    })
})