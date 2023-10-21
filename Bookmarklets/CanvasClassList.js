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
      j--; // Adjust the index because of the splice
    }
  }
}

// Step 3: Prompt the teacher with the final list
const result = JSON.stringify(studentList);

if (duplicates.length > 0) {
  alert("Duplicates found: " + JSON.stringify(duplicates));
} else {
  prompt("v  Copy the JSON list of students below  v", JSON.stringify(studentList));
}
