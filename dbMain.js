function createDatabase() {
    executeAction("createDB");
}

function showTables() {
    executeAction("showTables");
}

function showConfirmation() {
    // Show the confirmation modal
    const confirmationModal = document.getElementById("confirmation-modal");
    confirmationModal.style.display = "block";
}

function hideConfirmation() {
    // Hide the confirmation modal
    const confirmationModal = document.getElementById("confirmation-modal");
    confirmationModal.style.display = "none";
}

function deleteDatabase() {
    const host = document.getElementById("host").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const database = document.getElementById("database").value;

    // Close the confirmation modal
    hideConfirmation();

    // Send 'y' as the confirmation status
    executeAction("deleteDatabase", 'y');
}

function testConnection(){
    executeAction("testConnection")
}

function executeAction(action) {
    const host = document.getElementById("host").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const database = document.getElementById("database").value;

    // Create a FormData object to send data to the CGI script
    const formData = new FormData();
    formData.append("action", action);
    formData.append("host", host);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("database", database);
    formData.append("isConfirmed", 'y');

    fetch("/Sotonye_DBM_project/Python_works/DBM_package/cgi-bin/dbCRUD.py", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("response").innerHTML = data;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
