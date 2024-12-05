// function that returns a new subtask field
function get_subtask() {

  const main_div = document.createElement("div");
  main_div.className = "form-row";

  const subtask_div = document.createElement("div");
  subtask_div.className = "col-sm-6 mb-2";

  const delete_div = document.createElement("div");
  delete_div.className = "col-sm-4 mb-3";


  const subtask_input = document.createElement("input");
  subtask_input.className = "form-control subtask";
  subtask_input.placeholder = "Subtask";
  subtask_input.required = true;
  subtask_input.type = "text";

  subtask_div.append(subtask_input);

  const delete_button = document.createElement("button");
  delete_button.innerHTML = "Delete";
  delete_button.className = "delete btn btn-outline-secondary";

  delete_div.append(delete_button);

  main_div.append(subtask_div);
  main_div.append(delete_div);

  return main_div;
}

// AFTER LOADED PAGE
document.addEventListener("DOMContentLoaded", () => {

    console.log("loaded page");

    // HANDLE Add Task button CLICK
    document.querySelector("#addtask").onclick = () => {
      console.log("add task clicked");

      const subtasks = document.querySelector("#subtasks");
      subtasks.append(get_subtask());

      return false;
    };


    // HANDLE Delete button CLICK
    document.addEventListener("click", (event) => {
      const element = event.target;
      if (element.className === "delete btn btn-outline-secondary")  {
        console.log("clicked delete button");
        subtask = element.parentElement.parentElement;
        subtasks_div = subtask.parentElement;

        if (subtasks_div.children.length > 2) {
          console.log(subtasks_div.children.length);
          subtask.remove();
        }
        
        else {
          alert("Your Task should have atleast one subtask.");
        }

        event.preventDefault();
      }
    });


    // HANDLE Form Submission
    document.querySelector("#new-task-form").onsubmit = (event) => {
      console.log("Form submitted");

      const task_name = document.querySelector("#task").value;
      const task_description = document.querySelector("#description").value;
      const task_urgent = document.querySelector("#urgent").checked;
      const task_important = document.querySelector("#important").checked;


      let subtasks = [];
      document.querySelectorAll(".subtask").forEach((inp) => {
        subtasks = [...subtasks, inp.value];
      });

      const task = {
        name: task_name,
        description: task_description,
        subtasks: subtasks,
        urgent: task_urgent,
        important: task_important,
      };

      // POSTING TASK
      console.log("Posting Task");
      console.log(task);

      fetch("", {
        method:"post",
        body:JSON.stringify(task),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        const app = document.querySelector("#app");
        if (data["result"] == "success") {
          app.innerHTML = `
            <div id="completed" class="mx-3 my-3">
              <h1> ✅️ Task added Successfully </h1>
              <div class="ml-1"> <a href="/"> Go to tasks -> </a> </div>
            </div>
          `
        }
      });

      return false;
    };

});