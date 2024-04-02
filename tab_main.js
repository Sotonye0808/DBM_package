function createTable() {
    executeActiont("createTable");
}

function readTable(){
    executeActiont("readTable");
}

function showColumns(){
    executeActiont("showColumns");
}
//show modal for addColumns method
function addColumns(){
    const addColumnsModal = document.getElementById("addColumnsQ");
    addColumnsModal.style.display = "block";
}
//close modal for addColumns method
function closeDialog() {
    const addColumnsModal = document.getElementById("addColumnsQ");
    addColumnsModal.style.display = "none";
}
//show modal for changing columns
function changeColumnsQ() {
    const changeColumnsModal = document.getElementById("changeColumnsQ");
    changeColumnsModal.style.display = "block";
}
//close modal for changing columns
function closeDialogC() {
    const changeColumnsModal = document.getElementById("changeColumnsQ");
    changeColumnsModal.style.display = "none";
}
//show modal for adding columns
function addNewColumnQ() {
    const addNewColumnModal = document.getElementById("addNewColumnQ");
    addNewColumnModal.style.display = "block";
}
//close modal for adding columns
function closeDialogA() {
    const addNewColumnModal = document.getElementById("addNewColumnQ");
    addNewColumnModal.style.display = "none";
}
//function to execute changeColumns
function changeColumns() {
    closeDialog();
    executeActiont("changeColumns");
}

//function to execute addNewColumn
function addNewColumn() {
    closeDialog();
    executeActiont("addNewColumn");
}
//for table deletion
function showConfirmationTab() {
    // Show the confirmation modal for deleting table
    const delTabConfirmationModal = document.getElementById("delTabModal");
    delTabConfirmationModal.style.display = "block";
}
function hideConfirmationTab() {
    // Hide the confirmation modal for deleting table
    const delTabConfirmationModal = document.getElementById("delTabModal");
    delTabConfirmationModal.style.display = "none";
}
function deleteTable() {

    // Close the confirmation modal
    hideConfirmationTab();

    // Send 'y' as the confirmation status
    executeActiont("deleteTable", 'y');
}

//functions for deleting columns
//show modal for deleteColumns method
function deleteColumnsQ(){
    const deleteColumnsModal = document.getElementById("deleteColumnsQ");
    deleteColumnsModal.style.display = "block";
}
//close modal for deleteColumns method
function closeDeleteColumnsDialog() {
    const addColumnsModal = document.getElementById("deleteColumnsQ");
    addColumnsModal.style.display = "none";
}
//show final confirmation modal to delete columns
function deleteColumnsConfirmation(){
    const deleteColumnsModal = document.getElementById("deleteColumnsModal");
    deleteColumnsModal.style.display = "block";
}
// hide confirmation modal for deleting columns
function hideConfirmationCol(){
    const deleteColumnsModal = document.getElementById("deleteColumnsModal");
    deleteColumnsModal.style.display = "none";
}
//function to actually delete columns
function deleteColumns() {

    // Close the confirmation modal
    hideConfirmationCol();

    // Send 'y' as the confirmation status
    executeActiont("deleteColumns", 'y');
}

//functions for deleting foreign keys
//for foreign keys form modal
function getForeignKeysModal(){
    const deleteFKModal = document.getElementById("deleteFKQ");
    deleteFKModal.style.display = "block";
}
function closeForeignKeysModal(){
    const deleteFKModal = document.getElementById("deleteFKQ");
    deleteFKModal.style.display = "none";
}
//for retrieving foreign keys as options
function getForeignKeys(){
    executeActiont("getForeignKeys");
}
//displaying final confirmation modal
function deleteForeignKeysConfModal(){
    const deleteFKConfModal = document.getElementById("deleteForeignKeysConfirmation");
    deleteFKConfModal.style.display = "block";
}
//hiding final conf. modal
function hideConfirmationFK(){
    const deleteFKConfModal = document.getElementById("deleteForeignKeysConfirmation");
    deleteFKConfModal.style.display = "none";
    getForeignKeys();
}
//dropping key constraints action
function deleteForeignKeyConstraints(){
    executeActiont("deleteForeignKeyConstraints");
}
//permanently delete foreign keys
function deleteForeignKeys(){
    executeActiont("deleteForeignKeys");
}

//
function executeActiont(actiont) {
    const host = document.getElementById("host").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const database = document.getElementById("database").value;
    const table = document.getElementById("table").value;
    const pk = document.getElementById("pk").value;
    const columnName = document.getElementById("columnName").value;
    const description = document.getElementById("description").value;
    const useDefaultDesc = document.getElementById("useDefaultDesc").checked;
    const makeForeignKey = document.getElementById("makeForeignKey").checked;
    const referencedColumn = document.getElementById("referencedColumn").value;
    const referencedTable = document.getElementById("referencedTable").value;
    const position = document.getElementById("position").value;
    const renameColumn = document.getElementById("renameColumn").checked;
    const changedName = document.getElementById("changedName").value;
    const afterColumn = document.getElementById("afterColumn").value;
    const newColumnName = document.getElementById("newColumnName").value;
    const newColumnDescription = document.getElementById("newColumnDescription").value;
    const useDefaultNewDesc = document.getElementById("useDefaultNewDesc").checked;
    const makeNewColumnForeignKey = document.getElementById("makeNewColumnForeignKey").checked;
    const referencedColumnAdd = document.getElementById("referencedColumnAdd").value;
    const referencedTableAdd = document.getElementById("referencedTableAdd").value;
    const newColumnPosition = document.getElementById("newColumnPosition").value;
    const newColumnAfter = document.getElementById("newColumnAfter").value;
    const columnNames = document.getElementById("columnNames").value;
    const foreignKeyConstraints = document.getElementById("foreignKeyConstraints").value
    // Create a FormData object to send data to the CGI script
    const formData = new FormData();
    formData.append("actiont", actiont);
    formData.append("host", host);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("database", database);
    formData.append("table", table);
    formData.append("pk", pk);
    formData.append("columnName", columnName);
    formData.append("description", description);
    formData.append("useDefaultDesc", useDefaultDesc);
    formData.append("makeForeignKey", makeForeignKey);
    formData.append("referencedColumn", referencedColumn);
    formData.append("referencedTable", referencedTable);
    formData.append("position", position);
    formData.append("afterColumn", afterColumn);
    formData.append("renameColumn", renameColumn);
    formData.append("changedName", changedName);
    formData.append("newColumnName", newColumnName);
    formData.append("newColumnDescription", newColumnDescription);
    formData.append("useDefaultNewDesc", useDefaultNewDesc);
    formData.append("makeNewColumnForeignKey", makeNewColumnForeignKey);
    formData.append("referencedColumnAdd", referencedColumnAdd);
    formData.append("referencedTableAdd", referencedTableAdd);
    formData.append("newColumnPosition", newColumnPosition);
    formData.append("newColumnAfter", newColumnAfter);
    formData.append("isConfirmedTab", 'y');
    formData.append("columnNames", columnNames);
    formData.append("isConfirmedCol", 'y');
    formData.append("foreignKeyConstraints", foreignKeyConstraints)

    fetch("/Sotonye_DBM_project/Python_works/DBM_package/cgi-bin/tabCRUD.py", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        if (actiont === "deleteColumns") {
            // Update the specific response div for the "Delete Columns" method
            document.getElementById("colDel").innerHTML = data;
        }
        else if (actiont === "changeColumns") {
            // Update the specific response div for the "Change Columns" method
            document.getElementById("responseChangeCol").innerHTML = data;
        }
        else if (actiont === "addNewColumn") {
            // Update the specific response div for the "Add Columns" method
            document.getElementById("responseAddNewCol").innerHTML = data;
        }
        else if (actiont === "getForeignKeys") {
            // display form for foreign key deletion in it's modal
            document.getElementById("FK_form").innerHTML = data;
        }
        else if (actiont === "deleteForeignKeyConstraints") {
            // display response for deleting foreign key constaints
            document.getElementById("FK_final").innerHTML = data;
        }
        else if (actiont === "deleteForeignKeys") {
            // display response for deleting foreign key constaints
            document.getElementById("FK_final").innerHTML = data;
        }
        else {document.getElementById("response").innerHTML = data;}
    })
    .catch(error => {
        console.error("Error:", error);
    });
}



