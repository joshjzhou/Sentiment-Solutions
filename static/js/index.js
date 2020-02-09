// $(function() {
//     $('#submit').click(function() {
//         user = {username:$('#input').val()};
//         $.ajax({
//             url: '/test',
//             data: JSON.stringify(user),
//             type: 'POST',
//             contentType: 'application/json; charset=utf-8',
//             dataType: 'json',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });
// });


var card = templater`
<div class="card mb-3 twitCard" >
    <div class="row no-gutters">
        <div class="col-md-3">
            <div class="row justify-content-center">
                <img src="${'profile_url'}" class="card-img"
                    alt="profile pic">
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-body">
                <h5 class="card-title">${'name'}</h5>
                <b><a href="https://www.twitter.com/${'username'}" target="_none" class="card-subtitle text-muted">@${'username'}</a></b>
                <br>
                <a class="btn btn-primary btn-sm" onClick="sendDM(this.id)" id="${'username'}" role="button" target="_none" style="color:white">Message</a>
            </div>
        </div>
        <div class="col-md-5">
            <div class="row justify-content-center">
                <div class="chart">
                    <svg viewBox="0 0 36 36" class="circular-chart orange">
                        <path class="circle-bg" d="M18 2.0845
                                                a 15.9155 15.9155 0 0 1 0 31.831
                                                a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <path class="circle" stroke-dasharray="${'avgscore'}, 100" d="M18 2.0845
                                                a 15.9155 15.9155 0 0 1 0 31.831
                                                a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <text x="18" y="20.35" class="percentage">${'avgscore'}%</text>
                    </svg>
                </div>
            </div>
            <div class="row justify-content-center">
                <p class="card-text"><small class="text-muted">${'status'}</small></p>
            </div>
        </div>
    </div>
</div>
`

function templater(strings, ...keys) {
return function(data) {
    let temp = strings.slice();
    keys.forEach((key, i) => {
        temp[i] = temp[i] + data[key];
    });
    return temp.join('');
}
};




// $("#inpt_search").on('focus', function () {
//     $(this).parent('label').addClass('active');
// });

// $("#inpt_search").on('blur', function () {
//     if ($(this).val().length == 0)
//         $(this).parent('label').removeClass('active');
// });

// $("#inpt_search").on("keypress", input => {
//     userList = {}
//     if (input.keyCode == 13) {
//         userAt = $('#inpt_search').val()
//         user = {username:$('#inpt_search').val()};
//         $.ajax({
//             url: '/test',
//             data: JSON.stringify(user),
//             type: 'POST',
//             contentType: 'application/json; charset=utf-8',
//             dataType: 'json',
//             success: function(response) {
//                 userList = response
//                 console.log(userList)
//                 search(userAt);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });



//         //$("#search-form").submit();
//         $("#inpt_search").val("");
//         $("#inpt_search").trigger('blur');


//         return false; // prevent the button click from happening
//     }
// });

// window.onload=function(){
//     console.log("here")
//     userAt = $('name').text();
//     user = {username:$('#name').text()};
//     console.log(user)
//         $.ajax({
//             url: '/test',
//             data: JSON.stringify(user),
//             type: 'POST',
//             contentType: 'application/json; charset=utf-8',
//             dataType: 'json',
//             success: function(response) {
//                 userList = response
//                 console.log(userList)
//                 search(userAt);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
// }


var userList = {}
$(document).ready(function() {

    
    
    userAt = $('#screen_name').text();
    user = {username:$('#screen_name').text()};
    $.ajax({
        url: '/test',
        data: JSON.stringify(user),
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            userList = response
            console.log(userList)
            search(userAt);
        },
        error: function(error) {
            console.log(error);
        }
    });

    
});



function search(username){
    console.log(username);
    //getRequest
    $('#resultCards').empty();
    //$("#search").addClass('triggered');
    //change the text and stuff

    //$("#name").text(userList[String(username)]);

    for(var user in userList){
        if(user != username){
            userList[user]['profile_url'] = userList[user]['profile_url'].replace('_normal', '');
            userList[user]['avgscore'] = 100 - parseInt(userList[user]['avgscore']);

            if(userList[user]['avgscore'] >= 75){
                userList[user]['status'] = "High Risk"
            }
            else if(userList[user]['avgscore'] >= 50){
                userList[user]['status'] = "Moderate Risk"
            }
            else if(userList[user]['avgscore'] >= 50){
                userList[user]['status'] = "Low Risk"
            }
            else{
                userList[user]['status'] = "No Risk"
            }
            

            $("#resultCards").append(card(userList[user]));
        }
    }
    document.getElementById('loading').outerHTML = "";
    $("#results").fadeIn(1000);
};



function sendDM(username){
    
    (async () => {
        const { value: text } = await Swal.fire({
          input: 'textarea',
          title: 'Send a message!',
          inputPlaceholder: 'Type your message here...',
          inputAttributes: {
            'aria-label': 'Type your message here'
          },
          showCancelButton: true
        })
        
        if (text) {
           
            user = {username:username, text: text};
            //console.log(user)
            $.ajax({
                url: '/dm',
                data: JSON.stringify(user),
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function(response) {
                    resp = response
                    //console.log(resp)
                    if(resp['status'] == 'success'){
                        Swal.fire({
                          icon: 'success',
                          title: 'Success!',
                          text: 'Message sent successfully!',
                        })
                    }
                    else{
                        Swal.fire({
                          icon: 'error',
                          title: 'Oops...',
                          text: 'Message failed to send',
                        })
                    }
                },
                error: function(error) {
                    console.log(error)
                    Swal.fire({
                          icon: 'error',
                          title: 'Oops...',
                          text: 'Message failed to send',
                        })
                }
            });
        }
    })()
}




/*
get request returns array of users with:
    Name
    username
    age?
    risk %
    dm link
*/
