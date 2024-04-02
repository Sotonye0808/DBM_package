//theme change code
var darken = document.getElementById("darken");

if(localStorage.getItem("theme") == null){
    localStorage.getItem("theme", "light");
};

localStorage.getItem("theme", "light");

let localData = localStorage.getItem("theme");
if(localData == "light"){
    document.body.classList.remove("darks");
} else if(localData == "dark"){
    darken.classList.toggle("active");
    document.body.classList.add("darks");
};

darken.onclick = function toggledark(){
    document.body.classList.toggle("darks");

    if(document.body.classList.contains("darks")){
        darken.classList.toggle("active");
        localStorage.setItem("theme", "dark");
    } else{
        darken.classList.toggle("active");
        localStorage.setItem("theme", "light");       
    };
};

// to the top smoothener
document.addEventListener("DOMContentLoaded", function() {
    var toTop = document.getElementById("toTop");
  
    toTop.style.display = "none";
  
    toTop.addEventListener("click", function(event) {
      event.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    });
  
    window.addEventListener("scroll", function() {
      if (window.scrollY > 100) {
        toTop.style.display = "block";
      } else {
        toTop.style.display = "none";
      }
    });
  });