let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function slideTrans(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("slide");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

function autoSlide() {
  let i;
  let slides = document.getElementsByClassName("slide");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  setTimeout(autoSlide, 3500); // Change image every 2 seconds
}
function test() {
  let section = document.getElementById("navigator");
  console.log(section);
}
function toggleDiv (divname) {
	let section = document.getElementById(divname); 
    console.log(section.innerHTML);
	if (section.style.display=="none") {
		section.style.display="block";
        console.log("on"); 
	}
	else {
		section.style.display="none";
        console.log("off");
	}
}
