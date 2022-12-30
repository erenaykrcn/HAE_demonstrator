function closee() {
    document.getElementById("pop-box").style.display = "none"
}

function circle_diameter() {
    outpu.value = parseInt(r.value)*parseInt(r.value)*3.14159265359;
}


function dropp() {
    //var myDropdown = document.getElementById("myDropdown");
    //if (myDropdown.style.display === "none") {
    //myDropdown.style.display = "block";}
    //if (myDropdown.style.display === "block") {
    //myDropdown.style.display = "none"}
    document.getElementById("myDropdown").classList.toggle("showw");
}

function dropp1() {
    document.getElementById("myDropdown1").classList.toggle("showw");
}

function dropp2() {
    document.getElementById("myDropdown2").classList.toggle("showw");
}


function openNav() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("mySidebar").style.width = "100%";
    try {
        window.clearInterval(setInt);
        window.clearInterval(setSl);
    } catch (e) {

    }
    try {
        document.getElementById("wall_up").style.display = "none";
        document.getElementsByClassName("uplo")[0].style.display = "none";
    } catch (e) {

    }
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("mySidebar").style.display = "none";
  try {
      setInt = window.setInterval(carousel, 3000);
      setSl = window.setInterval(slider,3000);
  } catch (e) {

  }

  try {
      document.getElementById("wall_up").style.display = "block";
      document.getElementsByClassName("uplo")[0].style.display = "block";
  } catch (e) {
  }
}

function show_sub0() {
    if (window.getComputedStyle(document.getElementById("acc_col0")).getPropertyValue("display")==="none") {
        document.getElementById("acc_col0").style.display = "block";
    } else {
        document.getElementById("acc_col0").style.display = "none";
    }
}

function show_sub1() {
    if (window.getComputedStyle(document.getElementById("acc_col1")).getPropertyValue("display")==="none") {
        document.getElementById("acc_col1").style.display = "block";
    } else {
        document.getElementById("acc_col1").style.display = "none";
    }
}



function search() {
    document.getElementsByClassName("search-input")[0].style.display = "block";
    document.getElementsByClassName("search-button")[0].style.marginRight = "1vw";
    document.getElementsByClassName("search-input")[0].style.width = "35vw";
    document.getElementsByClassName("search-input")[0].style.marginLeft = "-.1vw";
}

function not_search() {
    document.getElementsByClassName("search-button")[0].style.marginRight = "17vw";
    document.getElementsByClassName("search-input")[0].style.display = "none";
    document.getElementsByClassName("search-input")[0].style.marginLeft = "36vw";
    document.getElementsByClassName("search-input")[0].style.width = "1%";
}

function drop_nav() {
    document.getElementsByClassName("dropdown_myNav_wrapper")[0].style.height = "7vw";
}

function reverse_nav() {
    document.getElementsByClassName("dropdown_myNav_wrapper")[0].style.height = "0";
}

function account_p() {
    window.location = '/accounts/profile/'
}

function logout_a() {
    window.location = "/accounts/logout/"
}

function seeblogs_p() {
    window.location = "/posts/"
}

function postblogs_p() {
    window.location = "/posts/create/"
}

/*function myFunction() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = scrolled + "%";
  if (parseInt(document.body.scrollTop, 10)/parseInt(screen.height, 10) > 0.10) {
    document.getElementById("nav_div").style.position = "fixed";
    document.getElementById("nav_div").style.width = "74vw";
  } else {
    document.getElementById("nav_div").style.position = "relative";
  }
}*/

