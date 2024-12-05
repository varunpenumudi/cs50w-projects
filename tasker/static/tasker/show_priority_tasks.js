function get_task_html(task, radius) {
    return `
        <div class="task card d-flex flex-row align-items-center px-3 pt-2 mb-3">
            <div class="content w-75">
                <a href="/task/${task.id}" class="link-box">
                    <h4> ${task.name} </h4>
                    <div> 
                        <p class="mb-1"> ${task.description} </p>
                        <p> <small class="text-muted"> Last updated on ${task.last_updated} </small> </p>
                    </div>
                </a>
            </div>

            <div class="progress-div w-25 d-flex justify-content-end pl-2">
                <svg width="${(radius*2)+10}" height="${(radius*2)+10}">
                    <circle class="bg" cx="50%" cy="50%" r="${radius}" fill="none" 
                    stroke="black" stroke-width="6.5"
                    stroke-dasharray="${4*Math.PI*radius}"
                    />
                    <text x="53%" y="52%" dominant-baseline="middle"> ${task.progress}% </text>
                    <circle class="white-cover" cx="50%" cy="50%" r="${radius}" fill="none" 
                    stroke="aliceblue" stroke-width="5"
                    stroke-dasharray="${(2*Math.PI)*radius} ${(2*Math.PI)*radius}"
                    stroke-dashoffset="-${(task.progress/100)*(2*Math.PI*radius)}"
                    />
                </svg>

            </div>
        </div>
    `;
}


document.addEventListener("DOMContentLoaded", () => {

    const taskboard = document.querySelector("#taskboard");
    const priority = taskboard.dataset.priority;
    const page = taskboard.dataset.page;

    // radius
    const radius = 25;

    // fetch the tasks api for tasks for given priority
    fetch(`/api/tasks/priority/${priority}?page=${page}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        tasks = data.tasks;

        tasks.forEach((task) => {
            taskboard.innerHTML += get_task_html(task, radius);
        });

        if (tasks.length > 0) {
            pagination_code = `
                <nav>
                    <ul class="pagination justify-content-center">
                        <li id="prev-li" class="page-item"><a id="prev-a" class="page-link" href="#">Previous</a></li>

                        <li class="page-item active"><a class="page-link"> Page ${data.page} </a></li>

                        <li id="next-li" class="page-item"><a id="next-a" class="page-link" href="#">Next</a></li>
                    </ul>
                </nav>
            `
            taskboard.innerHTML += pagination_code;

            const next_li = document.querySelector("#next-li");
            const next_a = document.querySelector("#next-a");
            if (data.has_next) {
                next_a.href = `?page=${parseInt(data.page) + 1}`;
            } else {
                next_li.className+=" disabled";
            }

            const prev_li = document.querySelector("#prev-li");
            const prev_a = document.querySelector("#prev-a");
            if (data.has_previous) {
                prev_a.href = `?page=${parseInt(data.page) - 1}`;
            } else {
                prev_li.className+=" disabled";
            }
        }
    });
});