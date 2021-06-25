// var comp_btn = document.getElementById('completed');
// var incomp_btn = document.getElementById('incompleted');

// comp_btn.addEventListener('click',function(e){
//     e.preventDefault();
//     comp_btn.className = "button"
//     incomp_btn.className = "button is-primary"
// })

// incomp_btn.addEventListener('click',function(e){
//     e.preventDefault();
//     incomp_btn.className = "button"
//     comp_btn.className = "button is-primary"
// })

var deleteBtn = document.getElementById('delete');
var errorPanel = document.getElementById('error_panel');
deleteBtn.addEventListener((e)=>{
   alert()
   e.preventDefault();
   errorPanel.style.display = "hidden";
})



