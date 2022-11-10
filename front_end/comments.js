// TODO: Remplacer la valeur de apiServerUrl avec l'url du serveur d'API
const apiServerUrl = 'http://<IP>:5000';

function postComment(){
    const nameInput = document.getElementById("name");
    const messageInput = document.getElementById("message");
    const btn = document.getElementById("post-comment");

    btn.addEventListener("click", () => {
        const name = nameInput.value;
        const message = messageInput.value;
        const date = (new Date()).toDateString();

        if (name == '' || message == ''){
            alert('Name or message is missing');
        }
        else{
            const json = JSON.stringify({name: name, message: message, date: date});
            axios.post(apiServerUrl + "/api/comment", json,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            ).then((response) => {console.log(response)}).catch(err => console.error(err));
            alert('Your message has been sent !');
        }
    });
}

function getComment(name, comment, date){
    return `
    <div class="tm-comment tm-mb-45">
        <figure class="tm-comment-figure">
            <img src="img/comment.png" alt="Image" class="mb-2 rounded-circle img-thumbnail">
            <figcaption class="tm-color-primary text-center">${name}</figcaption>
        </figure>
        <div>
            <p>
                ${comment}
            </p>
            <div class="d-flex justify-content-between">
                <span class="tm-color-primary">${date}</span>
            </div>
        </div>
    </div>
    `;
}

function getComments() {
    const promiseData = axios.get(apiServerUrl + "/api/comments").then(response => response.data).catch(err => console.error(err));
    promiseData.then(data=>{
        for(item of data){
            document.getElementById('get-comments').innerHTML += getComment(item.name, item.comment, item.date);
        }
    });
}

postComment();
getComments();

