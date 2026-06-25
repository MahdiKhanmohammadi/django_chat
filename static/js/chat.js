

const room_id = JSON.parse(document.getElementById('room_id').textContent)

const socket = new WebSocket(`ws://${window.location.host}/ws/room/${room_id}/`)
socket.onclose = function (e) {
    console.error('socket closed unexpectedly');
};



const message_inp = document.getElementById('inp_message');

message_inp.focus();
message_inp.onkeyup = function (e) {
    if (e.key === 'Enter') {
        document.getElementById('tynChatSend').click();
    }
};

document.getElementById('tynChatSend').onclick = function (e) {
    let message = JSON.stringify({ 'message': message_inp.value });
    socket.send(message);
    message_inp.value = "";
}

socket.onmessage = function (e) {
    const message_container = document.getElementById('tynReply');

    let receive_message = JSON.parse(e.data);
    let current_user_pk = JSON.parse(document.getElementById('profile_id').textContent)

    const messages = document.getElementById('tynReply').innerHTML;

    if (receive_message.author_id == current_user_pk) {
        var tag_message = `<div class="tyn-reply-item outgoing">
                                    <div class="tyn-reply-group">
                                        <div class="tyn-reply-bubble">
                                            <div class="tyn-reply-text"> ${receive_message.message} </div>
                                            <!-- .tyn-reply-text -->
                                            <ul class="tyn-reply-tools">
                                                <li>
                                                    <button class="btn btn-icon btn-sm btn-transparent btn-pill">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                            fill="currentColor" class="bi bi-emoji-smile-fill"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16M7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5M4.285 9.567a.5.5 0 0 1 .683.183A3.5 3.5 0 0 0 8 11.5a3.5 3.5 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683M10 8c-.552 0-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5S10.552 8 10 8">
                                                            </path>
                                                        </svg><!-- emoji-smile-fill -->
                                                    </button>
                                                </li><!-- li -->
                                                <li class="dropup-center">
                                                    <button class="btn btn-icon btn-sm btn-transparent btn-pill"
                                                        data-bs-toggle="dropdown">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                            fill="currentColor" class="bi bi-three-dots"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3">
                                                            </path>
                                                        </svg><!-- three-dots -->
                                                    </button><!-- toggle -->
                                                    <div class="dropdown-menu dropdown-menu-xxs">
                                                        <ul class="tyn-list-links">
                                                            <li>
                                                                <a href="#">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                                        height="16" fill="currentColor"
                                                                        class="bi bi-pencil-square" viewBox="0 0 16 16">
                                                                        <path
                                                                            d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z">
                                                                        </path>
                                                                        <path fill-rule="evenodd"
                                                                            d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z">
                                                                        </path>
                                                                    </svg><!-- pencil-square -->
                                                                    <span>Edit</span>
                                                                </a>
                                                            </li><!-- li -->
                                                            <li>
                                                                <a href="#">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                                        height="16" fill="currentColor"
                                                                        class="bi bi-trash" viewBox="0 0 16 16">
                                                                        <path
                                                                            d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
                                                                        </path>
                                                                        <path
                                                                            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
                                                                        </path>
                                                                    </svg><!-- trash -->
                                                                    <span>Delete</span>
                                                                </a>
                                                            </li><!-- li -->
                                                        </ul><!-- .tyn-list-links -->
                                                    </div><!-- .dropdown-menu -->
                                                </li><!-- li -->
                                            </ul><!-- .tyn-reply-tools -->
                                        </div><!-- .tyn-reply-bubble -->
                                    </div><!-- .tyn-reply-group -->
                                </div> `;
    } else {
        var tag_message = `<div class="tyn-reply-item incoming">
                                    <div class="tyn-reply-avatar">
                                        <div class="tyn-media tyn-size-md tyn-circle">
                                            <img src="${receive_message.profile_image}" alt="">
                                        </div>
                                    </div><!-- .tyn-reply-avatar -->
                                    <div class="tyn-reply-group">
                                        <div class="tyn-reply-bubble">
                                            <div class="tyn-reply-text"> ${receive_message.message} </div>
                                            <!-- .tyn-reply-text -->
                                            <ul class="tyn-reply-tools">
                                                <li>
                                                    <button class="btn btn-icon btn-sm btn-transparent btn-pill">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                            fill="currentColor" class="bi bi-emoji-smile-fill"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16M7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5M4.285 9.567a.5.5 0 0 1 .683.183A3.5 3.5 0 0 0 8 11.5a3.5 3.5 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683M10 8c-.552 0-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5S10.552 8 10 8">
                                                            </path>
                                                        </svg><!-- emoji-smile-fill -->
                                                    </button>
                                                </li><!-- li -->
                                                <li class="dropup-center">
                                                    <button class="btn btn-icon btn-sm btn-transparent btn-pill"
                                                        data-bs-toggle="dropdown">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                            fill="currentColor" class="bi bi-three-dots"
                                                            viewBox="0 0 16 16">
                                                            <path
                                                                d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3">
                                                            </path>
                                                        </svg><!-- three-dots -->
                                                    </button><!-- toggle -->
                                                    <div class="dropdown-menu dropdown-menu-xxs">
                                                        <ul class="tyn-list-links">
                                                            <li>
                                                                <a href="#">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                                        height="16" fill="currentColor"
                                                                        class="bi bi-pencil-square" viewBox="0 0 16 16">
                                                                        <path
                                                                            d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z">
                                                                        </path>
                                                                        <path fill-rule="evenodd"
                                                                            d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z">
                                                                        </path>
                                                                    </svg><!-- pencil-square -->
                                                                    <span>Edit</span>
                                                                </a>
                                                            </li><!-- li -->
                                                            <li>
                                                                <a href="#">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                                                                        height="16" fill="currentColor"
                                                                        class="bi bi-trash" viewBox="0 0 16 16">
                                                                        <path
                                                                            d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
                                                                        </path>
                                                                        <path
                                                                            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
                                                                        </path>
                                                                    </svg><!-- trash -->
                                                                    <span>Delete</span>
                                                                </a>
                                                            </li><!-- li -->
                                                        </ul><!-- .tyn-list-links -->
                                                    </div><!-- .dropdown-menu -->
                                                </li><!-- li -->
                                            </ul><!-- .tyn-reply-tools -->
                                        </div><!-- .tyn-reply-bubble -->
                                    </div><!-- .tyn-reply-group -->
                                </div>`;
    }

    document.getElementById('tynReply').innerHTML = tag_message + messages;

}