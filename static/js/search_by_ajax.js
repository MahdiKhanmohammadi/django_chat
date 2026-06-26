//  find contact
const search_inp = document.getElementById('search-username');
const container = document.getElementById('contact-container');
var contact_tag = ""

search_inp.onchange = function (e) {
    let query = search_inp.value;
    if (query.length >= 3) {
        $.ajax({
            url: '/contacts/find/',  // The URL of the Django view that handles the request
            type: 'POST',
            data: {
                'query': query,
            },
            success: function (response) {
                container.innerHTML = "";
                contact_tag = "";
                if (response.detail) {
                    alert(response.detail);
                } else {
                    response.contacts.forEach(contact => {

                        contact_tag += `<li>
                        <div class="tyn-media-group">
                            <div class="tyn-media">
                                <img src="${contact?.image_profile}" alt="">
                            </div><!-- .tyn-media -->
                            <div class="tyn-media-col">
                                <div class="tyn-media-row">
                                    <h6 class="name">${contact?.first_name} ${contact?.last_name}</h6>
                                </div>
                                <div class="tyn-media-row">
                                    <p class="content">@${contact.username}</p>
                                </div>
                            </div><!-- .tyn-media-col -->
                            <ul class="tyn-media-option-list me-n1">
                                <li class="dropdown">
                                    <button name="add-btn" onclick="add_contact(this)" value=${contact.username} class="btn btn-icon btn-white btn-pill">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                            fill="currentColor" class="bi bi-person-plus-fill" viewBox="0 0 16 16">
                                            <path
                                                d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6">
                                            </path>
                                            <path fill-rule="evenodd"
                                                d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5">
                                            </path>
                                        </svg><!-- person-plus-fill -->
                                    </button>
                                </li>
                            </ul><!-- .tyn-media-option-list -->
                        </div><!-- .tyn-media-group -->
                    </li>`
                    });
                    container.innerHTML = contact_tag;
                }
            }
        });
    };
}

// add contact

function add_contact(btn) {
    let username = btn.value;
    $.ajax({
        url: '/contacts/add/',  // The URL of the Django view that handles the request
        type: 'POST',
        data: {
            'username': username
        },
        success: function (response) {
            debugger;
            if (response.detail == true) {
                swal("Add !", "User added your contacts !", "success");
            } else {
                swal("Exist!", "contact already exist !", "info");
            }
        }

    });
}