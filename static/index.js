var prev_slot_date = "";
const interval = setInterval(() => {
  fetch("/update")
    .then(response => response.json())
    .then(data => {
      console.log(data);
      const slot_date_field = document.getElementById("slot_date");
      const updated_at_field = document.getElementById("updated_at");
      slot_date_field.innerText = data.slot_date;
      updated_at_field.innerText = data.updated_at;

      if (prev_slot_date && prev_slot_date != data.slot_date){
        alert(`New slot date received: ${slot_date}`);
        prev_slot_date = data.slot_date;
      }
    });
}, 20000);



if (!localStorage.getItem('show_data_notice')){
  document.getElementById('toast-default').style.display = 'block';
  localStorage.setItem('show_notice', true);
}