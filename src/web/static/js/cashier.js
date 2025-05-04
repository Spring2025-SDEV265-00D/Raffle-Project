// ... existing code ...
const { API_BASE_URL } = window.ENV;

const referenceNumInput = document.querySelector("#referenceNum");
const numResult = document.getElementById("result");
const redeemBtn = document.querySelector("#redeemBtn");
const refundBtn = document.querySelector("#refundBtn");

// Helper to show a message
function showMessage(msg) {
  numResult.innerHTML = `<div class="text-2xl font-semibold">${msg}</div>`;
}

// Helper to perform redeem/refund
async function performAction(ticketId, action) {
  try {
    const url = `${API_BASE_URL}/redeem/ticket`;
    const response = await fetch(url, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ticket_id: ticketId,
        request: action,
      }),
    });

    if (response.status === 404) {
      return { error: "Ticket does not exist." };
    }

    const result = await response.json();
    return result;
  } catch (err) {
    return { error: "Network error while processing request." };
  }
}

async function handleAction(action) {
  numResult.innerHTML = "";
  const ticketId = referenceNumInput.value.trim();
  if (!ticketId) {
    showMessage("Please enter a reference number.");
    return;
  }

  // Step 2: Redeem or Refund
  const result = await performAction(ticketId, action);
  if (result.error) {
    showMessage(result.error);
    return;
  }

  showMessage(result.message);
}

redeemBtn.addEventListener("click", () => handleAction("redeem"));
refundBtn.addEventListener("click", () => handleAction("refund"));
