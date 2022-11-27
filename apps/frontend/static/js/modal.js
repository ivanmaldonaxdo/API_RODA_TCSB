let cerrar =document.querySelectorAll(".close")[0];
let modal =document.querySelectorAll(".amodal")[0];
let modalc =document.querySelectorAll(".modal-container")[0];
let abrir =document.querySelectorAll(".ctacli")[0];



abrir.addEventListener("click", function(e){
    e.preventDefault();

    modalc.style.opacity = "1";
    modalc.style.visibility = "visible";
    modal.classList.toggle("modal-close");

});



cerrar.addEventListener("click", function(){
    modal.classList.toggle("modal-close");

    setTimeout(function() {
        modalc.style.opacity = "0";
        modalc.style.visibility = "hidden";
    }, 600);

});

window.addEventListener("click", function (e){
    if(e.target == modalc){
        modal.classList.toggle("modal-close");

        setTimeout(function() {
            modalc.style.opacity = "0";
            modalc.style.visibility = "hidden";
        }, 600);
    }
})


// const open = document.getElementById('open');
// const comentario_ = document.getElementById('comentario_');
// const close = document.getElementById('close');

// open.addEventListener('click',() =>{
//     comentario_.classList.add('show');
    
// });

// close.addEventListener('click',() =>{
//     comentario_.classList.remove('show');
// });

