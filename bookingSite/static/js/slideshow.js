//https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_slideshow
var currentIndex = 1; //current slide
showSlides(currentIndex);

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("slide");
  var dots = document.getElementsByClassName("dot");
  var captions = document.getElementsByClassName("caption");
  if (n > slides.length) {
    currentIndex = 1;
  }
  else if (n < 1) {
    currentIndex = slides.length;
  }
  //hide all elements
  for (i = 0; i < slides.length; ++i) {
    slides[i].style.display = "none";
    dots[i].className = dots[i].className.replace(" active", "");
    captions[i].style.display = "none";
  }
  //reveal current elements
  captions[currentIndex - 1].style.display = "block";
  slides[currentIndex - 1].style.display = "block";
  dots[currentIndex - 1].className += " active";
}

function plusSlides(n) {
  showSlides(currentIndex += n);
}

function currentSlide(n) {
  showSlides(currentIndex = n);
}
