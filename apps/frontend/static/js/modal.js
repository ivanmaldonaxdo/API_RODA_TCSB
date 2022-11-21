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




const open = document.getElementById('open');
const comentario_ = document.getElementById('comentario_');
const close = document.getElementById('close');

open.addEventListener('click',() =>{
    comentario_.classList.add('show');
    
});

close.addEventListener('click',() =>{
    comentario_.classList.remove('show');
});


function nComentario(){
    let li = document.createElement("li")
    let valoringresado = document.getElementById("nuevoComentario").value;
    let text = document.createTextNode(valoringresado);
    li.appendChild(text);

    if(valoringresado==''){
            alert("Ingrese un comentario!")

    }else{
        document.getElementById("comentarios").appendChild(li);
    }

    document.getElementById("nuevoComentario").value = "";
    li.className ="comentarioa"
    
    let a = document.querySelectorAll(".contenedor-2")[0];
    a.style.opacity = "1";


    let borrar = document.createElement("p");
    borrar.innerHTML = ("Borrar")
    borrar.className ="borra";
    li.appendChild(borrar)

    let borra = document.getElementsByClassName("borra");
    let i 
    for (i=0; i < borra.length; i ++){
        borra[i].onclick = function(){
            let div = this.parentElement;
            div.style.display = "none";
        }
    }
}