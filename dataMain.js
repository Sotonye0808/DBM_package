function addRecords() {
    executeActiond("addRecords");
}
function displayKeys() {
    executeActiond("displayKeys");
}
function displayRecords() {
    executeActiond("displayRecords");
}
//show modal for searching records
function searchRecordsQ() {
    const searchRecordsModal = document.getElementById("searchRecordsQ");
    searchRecordsModal.style.display = "block";
}
//close modal for searching records
function closeSearchRecordsQ() {
    const searchRecordsModal = document.getElementById("searchRecordsQ");
    searchRecordsModal.style.display = "none";
}
//function to execute searchRecords
function searchRecords() {
    executeActiond("searchRecords");
}

//show modal for query operations
function executeQueryQ() {
    const executeQueryModal = document.getElementById("executeQueryQ");
    executeQueryModal.style.display = "block";
}
//close modal for query operations
function closeExecuteQueryQ() {
    const executeQueryModal = document.getElementById("executeQueryQ");
    executeQueryModal.style.display = "none";
}
//function to query operations
function executeQuery() {
    executeActiond("executeQuery");
}
//show modal for join operations
function performJoinQ() {
    const performJoinModal = document.getElementById("performJoinQ");
    performJoinModal.style.display = "block";
}
//close modal for query operations
function closePerformJoinQ() {
    const performJoinModal = document.getElementById("performJoinQ");
    performJoinModal.style.display = "none";
}
//function to query operations
function performJoin() {
    executeActiond("performJoin");
}

//for delete rows
//show modal for delete rows
function deleteRowsQ() {
    const deleteRowsModal = document.getElementById("delRowModal");
    deleteRowsModal.style.display = "block";
}
//close modal for delete rows
function closeDeleteRowsQ() {
    const deleteRowsModal = document.getElementById("delRowModal");
    deleteRowsModal.style.display = "none";
}
//function to delete rows
function deleteRows() {
    executeActiond("deleteRows");
    closeDeleteRowsQ()
}

//for delete records
//show modal for delete records
function deleteRecordsQ() {
    const deleteRecordsModal = document.getElementById("delRecordsModal");
    deleteRecordsModal.style.display = "block";
}
//show modal for delete records confirmation
function deleteRecordsConfirm() {
    const deleteRecordsModal = document.getElementById("delRecordsConfirm");
    deleteRecordsModal.style.display = "block";
}
//close modal for delete records
function closeDeleteRecordsQ() {
    const deleteRecordsModal = document.getElementById("delRecordsModal");
    deleteRecordsModal.style.display = "none";
}
//close modal for delete records confirmation
function closeDeleteRecordsConfQ() {
    const deleteRecordsConfirm = document.getElementById("delRecordsConfirm");
    deleteRecordsConfirm.style.display = "none";
}
//function to delete records
function deleteRecords() {
    executeActiond("deleteRecords");
    closeDeleteRecordsConfQ();
}

//function to update records
function updateRecords() {
    executeActiond("updateRecords");
}
//
function executeActiond(actiond) {
    const host = document.getElementById("host").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const database = document.getElementById("database").value;
    const table = document.getElementById("table").value;
    const pk = document.getElementById("pk").value;
    const primaryKeys = document.getElementById("primaryKeys").value;
    const dataColumnNames = document.getElementById("dataColumnNames").value;
    const dataColumnValues = document.getElementById("dataColumnValues").value;
    const searchColumnName = document.getElementById("searchColumnName").value;
    const searchChar = document.getElementById("searchChar").value;
    const searchOptions = document.getElementById("searchOptions").value;
    const queryOptions = document.getElementById("queryOptions").value;
    const columnsToConcat = document.getElementById("columnsToConcat").value;
    const separatorChar = document.getElementById("separatorChar").value;
    const concatColumnName = document.getElementById("concatColumnName").value;
    const displayColumns = document.getElementById("displayColumns").value;
    const columnsToDistinct = document.getElementById("columnsToDistinct").value;
    const columnToRange = document.getElementById("columnToRange").value;
    const lowerBound = document.getElementById("lowerBound").value;
    const upperBound = document.getElementById("upperBound").value;
    const joinType = document.getElementById("joinType").value;
    const numTablesToJoin = document.getElementById("numTablesToJoin").value;
    const tablesToJoin = document.getElementById("tablesToJoin").value;
    const primaryKeyColumns = document.getElementById("primaryKeyColumns").value;
    const foreignKeyColumns = document.getElementById("foreignKeyColumns").value;
    const joinColumnQ = document.getElementById("joinColumnQ").checked;
    const joinColumns = document.getElementById("joinColumns").value;
    const pkRange = document.getElementById("pkRange").checked;
    const startingPK = document.getElementById("startingPK").value;
    const endingPK = document.getElementById("endingPK").value;
    const specificColumnByPKRange = document.getElementById("specificColumnByPKRange").checked;
    const allInSpecificColumn = document.getElementById("allInSpecificColumn").checked;
    const allInTable = document.getElementById("allInTable").checked;
    const specificColumn = document.getElementById("specificColumn").value;
    

    // Create a FormData object to send data to the CGI script
    const formData = new FormData();
    formData.append("actiond", actiond);
    formData.append("host", host);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("database", database);
    formData.append("table", table);
    formData.append("pk", pk);
    formData.append("primaryKeys", primaryKeys);
    formData.append("dataColumnNames", dataColumnNames);
    formData.append("dataColumnValues", dataColumnValues);
    formData.append("searchColumnName", searchColumnName);
    formData.append("searchChar", searchChar);
    formData.append("searchOptions", searchOptions);
    formData.append("queryOptions", queryOptions);
    formData.append("columnsToConcat", columnsToConcat);
    formData.append("concatColumnName", concatColumnName);
    formData.append("displayColumns", displayColumns);
    formData.append("separatorChar", separatorChar);
    formData.append("columnsToDistinct", columnsToDistinct);
    formData.append("columnToRange", columnToRange);
    formData.append("lowerBound", lowerBound);
    formData.append("upperBound", upperBound); 
    formData.append("joinType", joinType);
    formData.append("numTablesToJoin", numTablesToJoin);
    formData.append("tablesToJoin", tablesToJoin);
    formData.append("primaryKeyColumns", primaryKeyColumns);
    formData.append("foreignKeyColumns", foreignKeyColumns);
    formData.append("joinColumnQ", joinColumnQ);
    formData.append("joinColumns", joinColumns);
    formData.append("pkRange", pkRange);
    formData.append("startingPK", startingPK);
    formData.append("endingPK", endingPK);
    formData.append("specificColumnByPKRange", specificColumnByPKRange);
    formData.append("allInSpecificColumn", allInSpecificColumn);
    formData.append("allInTable", allInTable);
    formData.append("specificColumn", specificColumn);
    

    fetch("/Sotonye_DBM_project/Python_works/DBM_package/cgi-bin/dataCRUD.py", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        if (actiond === "searchRecords") {
            // Update the specific response div for the "Search Records" method
            document.getElementById("searchRecordsResponse").innerHTML = data;
        }
        else if (actiond === "executeQuery") {
            // Update the specific response div for the "Execute Query" method
            document.getElementById("executeQueryResponse").innerHTML = data;
        }
        else if (actiond === "performJoin") {
            // Update the specific response div for the "Perform Join" method
            document.getElementById("performJoinResponse").innerHTML = data;
        }
        else if (actiond === "deleteRecords") {
            // Update the specific response div for the "Delete Records" method
            document.getElementById("recordDel").innerHTML = data;
        }
        else {document.getElementById("response").innerHTML = data;}
    })
    .catch(error => {
        console.error("Error:", error);
    });
}