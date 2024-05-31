



function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation);
        
}   else {
        console.log("Error in getting location");
}
}
function sendLocation(pos){
        lat = pos.coords.latitude;
        lon = pos.coords.longitude;
        console.log("Success in Part 1", lat, lon);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const data = {lat, lon};

        const options = {
            method:"POST", 
            
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify(data)
            
        };
        
        fetch('/', options);
    }        
       
       
        
      


