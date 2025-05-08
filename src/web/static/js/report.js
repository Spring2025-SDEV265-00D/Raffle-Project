const { API_BASE_URL } = window.ENV;


document.addEventListener("DOMContentLoaded", async function () {
    const reportForm = document.getElementById("getReportForm");
    const closeModalBtn = document.getElementById("closeModal");
    const printBtn = document.getElementById("printBtn");
  
    if (!reportForm) {
      console.error("Form #getReportForm not found in DOM.");
      return;
    }
  
    reportForm.addEventListener("submit", async function (event) {
      event.preventDefault();
      const raceID = document.getElementById("raceID").value;
  
      try {
        const response = await fetch(`${API_BASE_URL}/report/race`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ race_id: Number(raceID) }),
        });
  
        if (!response.ok) throw new Error("Network response was not ok");
  
        const reportData = await response.json();
        generateReportModal(raceID, reportData);
        document.getElementById("reportModal")?.classList.remove("hidden");
      } catch (error) {
        console.error("Error fetching race report:", error);
      }
    });
  
    if (closeModalBtn) {
      closeModalBtn.addEventListener("click", function () {
        document.getElementById("reportModal")?.classList.add("hidden");
      });
    }
  
    if (printBtn) {
      printBtn.addEventListener("click", function () {
        const reportContent = document.getElementById("reportContainer");
    
        if (!reportContent) {
          console.error("Report content is missing, cannot print.");
          return;
        }
        
        const printWindow = window.open('', '', 'width=800,height=600');
        printWindow.document.write('<html><head><title>Print Report</title><style>/* Add your CSS styles for the print layout here */</style></head><body>');
        printWindow.document.write(reportContent.innerHTML);
        printWindow.document.write('</body></html>');
        
        printWindow.document.close();
        printWindow.print();
        printWindow.close();
      });
    }
  });
  
async function generateReportModal(raceID, horseArray) {
  const container = document.getElementById("reportContainer");

  if (!Array.isArray(horseArray) || horseArray.length === 0) {
    container.innerHTML = `<p class="text-red-600">No report data available for race #${raceID}.</p>`;
    return;
  }

  container.innerHTML = `
    <h2 class="text-lg font-bold mb-4">Race Report for Race #${raceID}</h2>
    <div class="space-y-3">
      ${horseArray.map(horse => `
        <div class="border-b pb-2">
          <p><strong>Horse #${horse.horse_number}</strong></p>
          <p>Tickets Sold: ${horse.tickets_sold}</p>
          <p>Scratched: ${horse.scratched ? "Yes" : "No"}</p>
          <p>Winner: ${horse.winner ? "Yes" : "No"}</p>
        </div>
      `).join("")}
    </div>
  `;
}
