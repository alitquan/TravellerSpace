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
    console.log(section.clientHeight);
	if (section.style.display=="none") {
		section.style.display="block";
	}
	else {
		section.style.display="none";
	}
    console.log(section.clientHeight);
}


// for searching 

function passUserSearchQuery(query) {
  console.log("passUserSearchQuery executing");
  fetch ('/storeRenderQuery', {
    headers : {
      'Content-Type': 'application/json'
    },
    method:'POST',
    body: JSON.stringify({
      "render_query":query,
    })
  }).then(
    response => response.json() 
  ).then((data) => getUserPage(data)) 
  console.log("pusq done")
}


function getUserPage(data) {
  console.log(data)
  console.log("this is foo foo representing")
  console.log(data) 
  fetch('/return',{
    headers : {
      'Content-Type': 'application/json'
    },
    method:'POST',
    body: JSON.stringify({
      "searchedUser":data,
    }) 
  }).then(( response ) => {
    console.log("unparsed data")
    console.log(response)
    console.log(response.url) 
    window.location.href = response.url
    }).catch (console.error)
}


function updateList(names) { 
  var ul = document.getElementById("search-results");
  ul.innerHTML="";
  
  for (let i = 0; i < names.length; i++) { 
    var li = document.createElement("li");
    var anchor = document.createElement("a");
    anchor.appendChild(document.createTextNode(names[i]))
    anchor.classList.add("search-profile-link")
    let _anchor="javascript:passUserSearchQuery(\""+names[i]+"\");"
    anchor.href=_anchor
    li.appendChild(anchor) 
    ul.appendChild(li);
  }
}

function getResults() {

  let searchTerm = document.getElementById("bar").value; 
  let filter = document.getElementById("filters").value;

  query = "SELECT " + filter + " FROM Users where " +
      filter + " LIKE \'" + searchTerm + "%\';";

  fetch ('/getSearchTerm', {
    headers : {
      'Content-Type': 'application/json'
    },
    method:'POST',
    body: JSON.stringify({
      "search_term":searchTerm,
      "filter":filter,
      "query":query
    })
  }).then(function(response) { 
    return response.text();
  }).then(function(text) {
    console.log(searchTerm);
    console.log(filter);
    console.log(query);
    console.log('POST RESPONSE: ');
    console.log(text);
    console.log("In array form: \n");
    names = JSON.parse(text);
    console.log(names); 
    updateList(names);
  })
}


function updateProfile() {

	let bio = document.getElementById("p-input").value;
	console.log(bio)

	fetch('/updateProfile', {
		headers: {
			'Content-Type':'application/json'
		},
		method:'POST',
		body: JSON.stringify({
			"bio":bio
		})
	})

}


// pos 0 -- about. it has the edit bar
function togglePanel(target) {
	console.log("togglePanel()");
	let panels = document.querySelectorAll(".panel");
	let toggle = document.querySelectorAll(".panel-toggle");
	

	// store about panel height
	let aboutHeight = document.getElementById('container-profile').offsetHeight;
	console.log ("about height: " + aboutHeight); 

	// store navigator color
	let navigatorColor = document.getElementById('navigator').style.color;
	panels.forEach(function(panel, index) {
		panel.style.minHeight = aboutHeight + 'px';
		if (target == index) {
			panel.style.display = 'flex';
			console.log ("new min height: " + panel.style.minHeight);
			toggle[index].style.backgroundColor = 'blue'
		}
		else {
			toggle[index].style.backgroundColor = navigatorColor
			panel.style.display = 'none';
		}
	});

	let editBar = document.getElementById('edit-bar');

	// (un)hide edit bar
	if (target != 0) {
		editBar.style.display = 'none';
	}
	else {
		editBar.style.display = 'flex';
	}

}


function submitChat() { 
	let bar = document.getElementById("bar");
	let msg = document.getElementById("bar").value;
	fetch ('/submitChat', {
	    headers : {
	      'Content-Type': 'application/json'
	    },
	    method:'POST',
	    body: JSON.stringify({
	      "msg":msg,
	    })
	  })
	bar.value=""; 
} 


async function idToName (id) {
	try { 
		const param1 = id;
		const url = `/getUsername?id=${encodeURIComponent(param1)}`
		const name = await fetch(url);
		const ret = await name.json();
		console.log("This is the promise: ");
		console.log(ret); 
		return ret;
		// return JSON.stringify(ret);
	}
	catch (error) {
		console.error ('Errors: ', error);
	}
}

async function populateMessages(mJSON) {
    console.log("\npopulateMessages()");
    console.log(mJSON);
    console.log("populateMessages json done");
    let ul = document.getElementById("messages-list");

    for (const msg of mJSON) {
        let _username = await idToName(msg['userID']);
        let body = msg['body'];
        let _msg = "{username} : {msg}".replace("{msg}", body).replace("{username}", _username);
        var li = document.createElement("li");
        var para = document.createElement("p");
        para.innerText = _msg;
        li.classList.add("chat-msg");
        li.appendChild(para);
        ul.appendChild(li);
    }
}
