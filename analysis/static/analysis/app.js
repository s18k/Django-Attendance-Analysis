console.log("My app.js")

//If user adds a note add it to the local storage
window.onload = function () {

    let search = document.getElementById("searchTxt");
    console.log(search)
    search.addEventListener("input",function(){
        let inputVal=search.value;
        console.log(inputVal)
        let noteCards=document.getElementsByClassName('card');
        console.log(noteCards)
        Array.from(noteCards).forEach(function (element) {
            let cardTxt=element.getElementsByTagName("h5")[0].innerText;

            if(cardTxt.includes(inputVal))
            {
                console.log(cardTxt)
                element.style.display="block";
            }
            else{
                element.style.display="none";
            }



        })
    });

}