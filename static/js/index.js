document.addEventListener("DOMContentLoaded", function() {
  let canvas = document.getElementById("canvas");
  canvas.style.width = canvas.naturalWidth + "px";
  canvas.style.height = canvas.naturalHeight + "px";
  let imgSrc = document.getElementById("image").src//getAttribute("src");
  let imgName = imgSrc.split('/').pop(); // extract the file name from the URL
  console.log(imgName);
  // let imgPath = document.getElementById("image").getAttribute('src');
  // console.log(imgPath); // Add this line for debugging
  //console.log(imgSrc);

  const request = new XMLHttpRequest();
  canvas.addEventListener("dblclick", (e) => {
    let data = {
      x: e.offsetX,
      y: e.offsetY,
      name : imgName,
    };
    console.log("data:", data); // Add this line for debugging
    request.open("POST", `/coordinates/${JSON.stringify(data)}`);
    request.send();
  });
});