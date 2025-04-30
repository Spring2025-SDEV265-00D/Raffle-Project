
document.addEventListener("DOMContentLoaded", async function checkAdmin() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`,{
            method: "GET",
            credentials: "include"
            });
        if (!response.ok) {
            throw new Error("Failed to fetch auth role.");
        }

        const role = await response.text();
        console.log("Role:", role);

        if (role != "Admin") {
            if (role === "Cashier") {
                window.location.href = "/ticket/info";
            }
            else {
                window.location.href = "/event/selection";
            }
        }
        else {
            console.log("You are allowed to enter!")
        }
        }
    catch (error) {
            console.error("Error:", error);
            //Have this commented out until we have a login page.
            //window.location.href = "/login";
        }
});
        
