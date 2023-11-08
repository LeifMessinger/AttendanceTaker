(async function(){
  let scrollIntervalId = setInterval(function(){
     window.scrollBy(0, 10000)
  }, 1000);

  //This isn't reliable, because the loading sign only shows when it's fetching more results.
  function isLoading(){
    return (document.querySelector(".paginatedLoadingIndicator").style.getPropertyValue("display") != "none");
  }

  //So we'll just wait 10 seconds
  async function wait(ms, retVal){
      return new Promise((resolve, reject)=>{
          setTimeout(resolve, ms, retVal);
      });
  }

  await wait(10000);

  clearTimeout(scrollIntervalId);
  
  const users = Array.from(document.querySelectorAll(".rosterUser")).map((person)=>{
    return {"name": person.querySelector(".roster_user_name").textContent.trim(),
      "role": person.children[3].textContent.trim()
    };
  });
  
  // Step 1: Filter names where role is "Student" and remove pronouns
  const studentList = users
    .filter(user => user.role === "Student")
    .map(user => user.name.replace(/(\(.+\))/g, "").trim());
  
  // Step 2: Identify and handle duplicates
  const duplicates = [];
  for (let i = 0; i < studentList.length; i++) {
    for (let j = i + 1; j < studentList.length; j++) {
      if (studentList[i] === studentList[j]) {
        duplicates.push(studentList[i]);
        studentList.splice(j, 1);
        debugger
        j--; // Adjust the index because of the splice
      }
    }
  }
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
  
  // Step 3: Prompt the teacher with the final list
  const result = JSON.stringify(studentList);
  
  if (duplicates.length > 0) {
    alert("Duplicates found: " + JSON.stringify(duplicates));
  } else {
    copyString(result);
  }
  
  console.log(result);
})();
