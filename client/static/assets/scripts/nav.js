

function autocomplete(inp) {
    var currentFocus;
    inp.addEventListener("input", function (e) {
        var q = $(this).val();


        $.ajax({
            url: "{% url 'auto_complete' %}" + "?search=" + q,
            success: function (data) {

                closeAllLists();
                if (!q) {
                    return false;

                }
                currentFocus = -1;

                var arr = data.result[1]
                var a, b, i, val = this.value

                a = document.createElement("DIV");
                a.setAttribute("id", "autocomplete-list");
                a.setAttribute("class", "autocomplete-items");

                document.getElementById("myInput").parentNode.appendChild(a);
                /*for each item in the array...*/
                for (i = 0; i < arr.length; i++) {
                    b = document.createElement("DIV");

                    b.innerHTML += arr[i][0]

                    b.innerHTML += "<input type='hidden' value='" + arr[i][0] + "'>";

                    b.addEventListener("click", function (e) {

                        inp.value = this.getElementsByTagName("input")[0].value;
                        window.location.href = "{% url 'search_youtube' %}" + "?search=" + inp.value;
                        closeAllLists();
                    });
                    a.appendChild(b);
                }

            }
        });
    });

    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {

        console.log(e.keyCode)

        var x = document.getElementById("autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            console.log("Enter clicked" + currentFocus)

            if (currentFocus > -1) {

                /*and simulate a click on the "active" item:*/

                if (x) x[currentFocus].click();
            } else {
                if (inp.value) {
                    window.location.href = "{% url 'search_youtube' %}" + "?search=" + inp.value;
                }
            }
        }
    });

    function addActive(x) {

        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {

        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);

    });
}

function bar() {

}

function setGetParameter() {

    searchWord = document.getElementById('search').value;
    window.location.href = "{% url 'auto_complete' %}" + "?search=" + searchWord;
}


