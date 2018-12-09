var modal = document.getElementById('popuplogin')
/* Defines the modal */

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    /* If the user clicks off the modal it is set to invisible */
  }
}
