(async function(){
    const TEST = false;
    const COMMENT = false; //Don't actually click the submit button
    const CARE_IF_GRADED = false;
    const version = "v0.8";

    if(!(document.getElementById("comment_submit_button"))){
        alert("You need to be on the canvas SpeedGrader™ page for this to work.");
        return;
    }
    
    const listText = prompt("Enter the present JSON list");
    if(!listText) return;
    try{
        const presentList = JSON.parse(listText);
    }catch(e){
        alert("Couldn't parse list: " + e.message);
        return;
    }
    const presentList = JSON.parse(listText);
    
    let maxGrade = "100";
    const maxGradeElement = document.getElementById("grading-box-points-possible");
    if(!maxGradeElement){
        if(!confirm("Max grade not found. Defaulting to 100")){
            //If the user hits cancel
            return; //Quit the program
        }
    }else{
        const maxGradeText = maxGradeElement.textContent.trim();
        const outOfIndex = maxGradeText.indexOf("out of ");
        if(outOfIndex < 0){
            if(!confirm("Max grade not found. Defaulting to 100")){
                //If the user hits cancel
                return; //Quit the program
            }
        }
        maxGrade = maxGradeText.substr(outOfIndex + ("out of ").length);
    }

    async function wait(ms){
        return new Promise((resolve, reject)=>{
            setTimeout(resolve, ms);
        });
    }

    const studentSelectMenu = document.getElementById("students_selectmenu");
    for(let student of presentList){
        let found = false;
        for(let option of Array.from(studentSelectMenu.querySelectorAll("option"))){
            const optionText = option.textContent.trim();
            if(optionText.includes(student)){
                found = true;
                if((!CARE_IF_GRADED) || option.classList.contains("not_graded")){
                    option.selected = true;
                    studentSelectMenu.dispatchEvent(new Event('change'));
                    studentSelectMenu.dispatchEvent(new Event('input'));

                    await wait(300);
    
                    //Double check to make sure we are grading the right student
                    const nameElement = document.getElementById("students_selectmenu-button");
                    const name = nameElement.textContent.trim();
                    if(!(name.includes(student))){
                        alert("Something might have messed up with this student: " + student);
                    }else{
                        const gradingBox = document.getElementById("grading-box-extended");
                        if(!gradingBox){
                            alert("The grading box doesn't exist! How is that possible?");
                            return;
                        }
                        if(!TEST){
                            gradingBox.value = maxGrade;
                            gradingBox.dispatchEvent(new Event('change')); //This grades it
                        }

                        if(COMMENT){
                            const commentElement = document.getElementById("speed_grader_comment_textarea");
                            commentElement.value += "Graded using AttendanceTaker's speed grader autograder version " + version;
                            commentElement.dispatchEvent(new Event('change'));
                            commentElement.dispatchEvent(new Event('input'));
    
                            const submitButton = document.getElementById("comment_submit_button");
                            if(!submitButton){
                                alert("The submit button is gone!");
                                return;
                            }
                            
                            if(!test){
                                    submitButton.click(); //.click might not work here, and we might have to use .dispatchEvent(new Event('click'));
                            }
                        }
                        
                        await wait(500);
                    }
                }
            }
        }
        if(!found){
            alert("Student not found: " + student);
        }
    }
    alert("Done grading.");
})();
