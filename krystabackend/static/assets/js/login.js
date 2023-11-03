$(document).on('submit', '#loginform', function(event){
    event.preventDefault();
    debugger;
     let email = $('#email').val()
     let password =$('#password').val()
     csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
     
     let data = new FormData();
     data.append("email",email);
     data.append("password",password);
     data.append('csrfmiddlewaretoken',csrfmiddlewaretoken)
     
     $.ajax({
           url:"/",
           method: 'POST',
           processData:false,
           contentType:false,
           cache:false,
           mimeType:"multipart/form-data",
           data:data,
           success: function (response, status, xhr) {
            // Check the response status code
            if (xhr.status === 200) {
                // Successful login
                $('#loginform')[0].reset();
                window.location.href = '/orders/';
                
            } else {
                alert("Unexpected response status");
            }
        },
        error: function (xhr) {
            // Error occurred
            if (xhr.status === 400) {
                alert("Invalid username or password");
            } else {
                // Handle other error status codes if needed
                alert("Unexpected error");
            }
        }
           
       });
   
    });