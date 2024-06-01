
document.addEventListener("DOMContentLoaded", () => {

    // Edit post when the edit button is clicked
    document.addEventListener('click', (event) => {
        const element = event.target;

        if (element.className == 'edit-btn btn btn-primary btn-sm') {

            const post = element.parentElement.parentElement;
            let post_update_url = '';
            post_update_url = element.dataset.update_url;
            const content_div = post.querySelector(".content");
            const likes_and_timestamp = post.querySelector(".content-below-div");

            // show username of poster and hide everything else in post box.
            content_div.style.display = 'none';
            element.style.display = 'none';
            likes_and_timestamp.style.display = 'none';

            // textarea form_group
            const form_group = document.createElement("div");
            form_group.className = "form-group";   
            form_group.innerHTML = `<textarea class="form-control" id="content" rows="3">${content_div.innerHTML.trim()}</textarea>`;
            // Save button
            const save_button = document.createElement("button");
            save_button.className = "btn btn-primary btn-sm";  save_button.innerHTML = "Save";

            // Add textarea and save button elements to postbox.
            post.append(form_group);
            post.append(save_button);

            // Save the post
            save_button.onclick = () => {
                const new_content = form_group.querySelector("#content").value;

                // PUT request to update the post content
                fetch(post_update_url, {
                    method: "PUT",
                    body: JSON.stringify({
                        "content": new_content,
                    })
                })
                .then(response => response.json())
                .then(message => {
                    console.log(message);

                    // Show the actual post again with new content
                    if (message.result == "Success") {
                        content_div.innerHTML = new_content;
                        // Remove textarea and save button
                        form_group.remove();
                        save_button.remove();
                        // Show new content, likes, edit button and time stamp
                        content_div.style.display = 'block';
                        element.style.display = 'block';
                        likes_and_timestamp.style.display = 'flex';
                    }

                });
                
            };
        }
        
    });


    // Like or Unlike a post when heart icon is clicked.
    document.addEventListener('click', (event) => {
        const element = event.target;

        // Like currently unliked post.
        if (element.className === "bi bi-suit-heart") {

            likes_div = element.parentElement;
            like_url = element.dataset.like_url;
            cur_likes = parseInt( likes_div.querySelector(".likes-count").innerHTML );

            fetch(like_url, {
                method: "PUT",
                body: JSON.stringify({ like: true })
            })
            .then( response => response.json())
            .then( message => {
                console.log(message);
                if (message.result === "Success") {
                    likes_div.querySelector(".likes-count").innerHTML = cur_likes + 1;
                    element.className = "bi bi-suit-heart-fill";
                }
            });

        }
        // Unlike currently liked post
        else if (element.className === "bi bi-suit-heart-fill" ) {

            likes_div = element.parentElement;
            like_url = element.dataset.like_url;
            cur_likes = parseInt( likes_div.querySelector(".likes-count").innerHTML );

            fetch(like_url, {
                method: "PUT",
                body: JSON.stringify({ like: false })
            })
            .then( response => response.json())
            .then( message => {
                console.log(message);
                if (message.result === "Success") {
                    likes_div.querySelector(".likes-count").innerHTML = cur_likes - 1;
                    element.className = "bi bi-suit-heart";
                }
            });
        }
    });


})