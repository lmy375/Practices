
//http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php
url = ""

function callback2(){
	if (post_req.readyState == 4 && post_req.status ==200){
		console.log(post_req.responseText)
	}
}

function callback(){
	if (req.readyState == 4 && req.status ==200){
		var s = req.responseText
		console.log(s)
		var result = eval(s.substring(s.indexOf("<br/>")+6, s.indexOf("=<input")))
		console.log(result)

		post_req = new XMLHttpRequest()
		post_req.open("POST", url)
		post_req.setRequestHeader("Content-Type","application/x-www-form-urlencoded"); 
		post_req.onreadystatechange = callback2
		post_req.send("v="+ result)


	}
}

function http_get(){
	req = new XMLHttpRequest()
	req.open("GET", url)
	req.onreadystatechange = callback
	req.send()
}


//http_get()

//or just run this very quickly
f = document.forms[0]
s = f.innerText.split("\n")[1]
result = eval(s.substr(0,s.indexOf("=")))
console.log(result)
f.v.value = result
f.submit()
