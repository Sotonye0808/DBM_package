function executeDynamicQ() {
    // Show the confirmation modal
    const dynamicQueryConfirmModal = document.getElementById("dynamicQueryConfirm");
    dynamicQueryConfirmModal.style.display = "block";
}

function closeDynamicQueryConfQ() {
    // Hide the confirmation modal
    const dynamicQueryConfirmModal = document.getElementById("dynamicQueryConfirm");
    dynamicQueryConfirmModal.style.display = "none";
}

function queryDynamic() {
    // Close the confirmation modal
    closeDynamicQueryConfQ();
    executeActionq("queryDynamic");
}
function clearDynamic(){
    document.getElementById("dynamicQueryBox").value = "";
}

function executeActionq(actionq) {
    const host = document.getElementById("host").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const database = document.getElementById("database").value;
    const dynamicQueryBox = document.getElementById("dynamicQueryBox").value;

    // Create a FormData object to send data to the CGI script
    const formData = new FormData();
    formData.append("actionq", actionq);
    formData.append("host", host);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("database", database);
    formData.append("dynamicQueryBox", dynamicQueryBox);

    fetch("/Sotonye_DBM_project/Python_works/DBM_package/cgi-bin/queryCRUD.py", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("dynamicQueryResponse").innerHTML = data;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
