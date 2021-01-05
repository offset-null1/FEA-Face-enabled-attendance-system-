  
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true,
                audio: false,  
                video: {  
                    width: 600, height: 500  
          }   })
            .then(function (stream) {                                                    
                video.srcObject = stream;
                video.play();
             
            })
            .catch(function (error) {
                console.log(error)
                console.log("Something went wrong!");
            })
        }
      
      
        
      var video = document.querySelector("#video"); 
      var canvas = document.getElementById('canvas');
      var context = canvas.getContext('2d');
      imgArray = []

        function capture(){
            var i=0;
            var interval = setInterval(function(){
                context.drawImage(video, 0, 0);  
        
                var url =  canvas.toDataURL('image/png');
                var data_url=url.replace('data:image/png;base64,','');
                imgArray.push(data_url);
                console.log(imgArray[i]);
                i+=1;
                console.log(i);
                if(i==5){
                    clearInterval(interval);
                }
            },1000);
        };    
    
           
    function post(){
        document.getElementById('img').value = JSON.stringify(imgArray);
      }
      

    function redirect(){
        window.location.replace("http://localhost:5000/");
    }
