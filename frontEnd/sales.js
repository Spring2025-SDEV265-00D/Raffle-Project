document.querySelector("#createBtn").addEventListener("click", createTicket)

async function createTicket() {
    raceNum = document.querySelector("#raceNum").value

    if(raceNum > 0 && raceNum < 11) {
        
        document.querySelector("#results").innerHTML = '<img src="ticket.png" alt="Ticket">'
        document.querySelector("#clearDisplay").innerHTML = '<input col=100 class="createObjects" type="button" id="clearBtn" value="Clear"/>'
        document.querySelector("#clearBtn").addEventListener("click", printTicket)

    }
    else {
        document.querySelector("#error").innerHTML = "Please Choose Race Number"
    }

}

async function printTicket() {

    document.querySelector("#results").innerHTML = ''
    document.querySelector("#clearDisplay").innerHTML = ''
    document.querySelector("form").reset()
}