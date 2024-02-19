(async function(){

//So we'll just wait 10 seconds
async function wait(ms, retVal){
	return new Promise((resolve, reject)=>{
		setTimeout(resolve, ms, retVal);
	});
}

let roleSelect = document.querySelector('select[name="enrollment_role_id"]');
//For each of the options in the drop down
for(let child of Array.from(roleSelect.children)){
	if(child.textContent.trim().includes("Student (")){ //Because there's "Student Leader" with no students
		roleSelect.value = child.getAttribute("value");
		roleSelect.dispatchEvent(new Event("change"));
	}
}

await wait(1000);

let scrollIntervalId = setInterval(function(){
	window.scrollBy(0, 10000)
}, 1000);

//This isn't reliable, because the loading sign only shows when it's fetching more results.
function isLoading(){
	return (document.querySelector(".paginatedLoadingIndicator").style.getPropertyValue("display") != "none");
}

await wait(10000);

clearTimeout(scrollIntervalId);


let studentDB = {};
for(let student of Array.from(document.querySelectorAll(".rosterUser"))){
	//If this breaks, it's because that children[3] thing. The student id doesn't have a special class on it, so if something changes, then it breaks.
	studentDB[student.children[3].textContent.trim()] = student.querySelector(".roster_user_name").textContent.trim();
}

const listText = prompt("Enter the present JSON list");
if(!listText) return;
try{
	const presentList = JSON.parse(listText);
}catch(e){
	alert("Couldn't parse list: " + e.message);
	return;
}
const stuIDs = JSON.parse(listText);

function copyString(text){
	async function navigatorClipboardCopy(text){
			if(document.location.protocol != "https:"){
					return false;
			}
			return new Promise((resolve, reject)=>{
					navigator.clipboard.writeText(text).then(()=>{resolve(true);}, ()=>{resolve(false);});
			});
	}
	function domCopy(text){
			if(!(document.execCommand)){
					console.warn("They finally deprecated document.execCommand!");
			}

			const input = document.createElement('textarea');
			input.value = text;
			document.body.appendChild(input);
			input.select();
			const success = document.execCommand('copy');
			document.body.removeChild(input);

			return success;
	}
	function promptCopy(){
			prompt("Copy failed. Might have ... somewhere. Check console.", text);
			console.log(text);
	}
	function done(){
			alert("Copied to clipboard");
	}
	navigatorClipboardCopy(text).catch(()=>{return false;}).then((success)=>{
			if(success){
					done();
			}else{
					if(domCopy(text)){
							done();
					}else{
							promptCopy();
					}
			}
	});
}

let result = stuIDs.map(id=>studentDB[id]).map(name=>name.replace(/(\(.+\))/g, "").trim());

console.log(result);

copyString(JSON.stringify(result));

})();
