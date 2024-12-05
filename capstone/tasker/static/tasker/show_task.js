document.addEventListener('DOMContentLoaded', () => {

    // Handle the urgent checkbox click
    document.querySelector("#urgent-check").onchange = (event) => {
        checkbox = event.target;
        console.log(`urgent checkbox checked: ${checkbox.checked}`);

        // API call to make task urgent/ not urgent
        fetch(`/api/tasks/${checkbox.dataset.id}`, {
            method:"put",
            body: JSON.stringify({
                urgent: checkbox.checked,
            }),
        })
        .then(response => response.json())
        .then(message => {
            console.log(message);
        })
        .catch(err => {
            console.log(`Error: ${err}`);
        });
    }

    // Handle the important checkbox click
    document.querySelector("#important-check").onchange = (event) => {
        checkbox = event.target;
        console.log(`important checkbox checked: ${checkbox.checked}`);

        // API call to make task important/ not important
        fetch(`/api/tasks/${checkbox.dataset.id}`, {
            method:"put",
            body: JSON.stringify({
                important: checkbox.checked
            }),
        })
        .then(response => response.json())
        .then(message => {
            console.log(message);
        })
        .catch(err => {
            console.log(`Error: ${err}`);
        });
    }


    // When task description edit button is clicked
    document.addEventListener('click', (event) => {
        if (event.target.id == "edit-description-button"){
            description_edit_btn = event.target;
            desc_paragraph = document.querySelector("#task-description");

            // get the current description and task id
            current_description = desc_paragraph.innerHTML;
            task_id = description_edit_btn.dataset.id;
    
            // Hide the edit button and description paragraph
            desc_paragraph.style.display = "none";
            description_edit_btn.style.display = "none";
    
            edit_desc_form = `
                <form id="edit-desc-form" class="form">
                    <textarea class="form-control mb-3" id="description-textarea" rows="2">${current_description.trim()}</textarea>
                    <button id="save-desc" class="btn btn-primary"> Save </button>
                </form>
            `
            document.querySelector("#description-div").innerHTML += edit_desc_form;
    
            document.querySelector("#save-desc").onclick = () => {
                const new_desc = document.querySelector("#description-textarea").value;
    
                // API call to update task description
                fetch(`/api/tasks/${task_id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        description: new_desc,
                    })
                })
                .then(response => response.json())
                .then(message => {
                    console.log(message);
    
                    document.querySelector("#task-description").innerHTML = new_desc;
    
                    // hide the edit description form
                    document.querySelector("#edit-desc-form").remove();
    
                    document.querySelector("#task-description").style.display = 'block';
                    document.querySelector("#edit-description-button").style.display = 'block';
                })
                .catch(err => {
                    console.log(`Error ${err}`);
    
                });
    
                return false;
            };
        }
    });


    // When clicked on a checkbox
    document.addEventListener('click', (event) => {
        if (event.target.className == "subtask-check form-check-input") {
            checkbox = event.target;
            let subtask_id = checkbox.dataset.id;

            console.log( "subtask", subtask_id, "completed: ", checkbox.checked);

            // API call to make the subtask completed/not completed
            fetch(`/api/subtask/${subtask_id}`, {
                method: "PUT",
                body: JSON.stringify( {
                    completed: checkbox.checked,
                }),
            })
            .then(response => response.json())
            .then(message => {
                console.log(message);
                task_progress = message.new_progress;

                document.querySelector(".progress-bar").style.width = `${task_progress}%`;
                document.querySelector(".progress-bar").innerHTML = `${task_progress}%`;
            })
            .catch(err => {
                console.log(`Error: ${err}`);
            });
        }
    });


    // Delete a subtask when the delete button is clicked
    document.addEventListener('click', (event) => {
        target = event.target;
        
        if (target.className == "subtask-delete-button btn btn-sm btn-outline-danger") {
            const subtask_container = target.parentNode.parentNode;

            if (subtask_container.parentNode.children.length <= 2)  {
                alert("You cannot delete this, a Task should have atleast 1 subtask.");
                return;
            }
            const subtask_id = subtask_container.dataset.id;

            // Api request to delete subtask
            fetch(`/api/subtask/${subtask_id}`, {
                method:"delete",
                body: JSON.stringify(),
            })
            .then(response => response.json())
            .then(message => {
                console.log(message);
                task_progress = message.new_progress;

                document.querySelector(".progress-bar").style.width = `${task_progress}%`;
                document.querySelector(".progress-bar").innerHTML = `${task_progress}%`;
            })
            .catch(err => {
                console.log(`Error Occured: ${err}`);
            });

            subtask_container.remove();
        }
    })


    // enable the add task button only when writing on it
    const input = document.querySelector('#subtask-input');
    const add_subtask_btn = document.querySelector("#add-btn");
    add_subtask_btn.disabled = true;

    input.onkeyup = () => {
        if (input.value != "") {
            add_subtask_btn.disabled = false
        } else {
            add_subtask_btn.disabled = true;
        }
    }


    // Add a subtask when add subtask form is submitted
    document.querySelector('#add-subtask-form').onsubmit = (event) => {
        const form = event.target;
        const subtask_name = form.querySelector("input").value;
        const task_id = form.dataset.taskid;

        const subtask = {
            subtask_name: subtask_name,
            taskid: task_id,
        }

        // API request to add the subtask
        fetch("/api/subtask/add", {
            method: "post",
            body: JSON.stringify(subtask),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);

            // creating div for showing subtask just created
            const subtask_div = document.createElement("div");
            subtask_div.className = "subtask border rounded p-2 mb-2 w-75 d-flex flex-row justify-content-between align-items-center";
            subtask_div.dataset.id = data.subtask.id;
            const subtask_html = `
                    <div class="subtask-checkbox ml-4 mb-2">
                        <input class="subtask-check form-check-input" type="checkbox" id="cb${data.subtask.id}" data-id="${data.subtask.id}">
                        <label class="form-check-label ml-2 mt-1 text-capitalize" for="cb${data.subtask.id}"> ${subtask.subtask_name} </label>
                    </div>
                    <div>
                        <button class="subtask-delete-button btn btn-sm btn-outline-danger"> Delete </button>
                    </div>
            `
            subtask_div.innerHTML = subtask_html;

            document.querySelector("#subtasks-container").append(subtask_div);
            task_progress = data.new_progress;

            document.querySelector(".progress-bar").style.width = `${task_progress}%`;
            document.querySelector(".progress-bar").innerHTML = `${task_progress}%`;
        })
        .catch(err => {
            console.log(`Error Occured: ${err}`);
        });

        // clear the input field and disable add task button
        form.querySelector("input").value = '';
        form.querySelector("button").disabled = true;
        return false;
    }

});