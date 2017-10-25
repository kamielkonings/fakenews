fetch("http://corset.herokuapp.com/?url=https://www.demorgen.be/rss.xml")
  .then(res => res.text())
  .then(text => {
    return new window.DOMParser().parseFromString(text, "text/xml");
  })
  .then(data => {
    console.log(data);
    window.data = data;
    const items = data.querySelectorAll("item");
    for (let item of items) {
      const title = item.querySelector("title").textContent;
      let h1 = document.createElement("p");
      h1.innerHTML = title;
      document.body.appendChild(h1);

      const images = item.getElementsByTagName("content:encoded");
      if (images.length > 0) {
        const image = images[0].textContent;

        if (image) {
          let img = document.createElement("img");
          img.setAttribute("src", image);
          //document.body.appendChild(img);
        }
      }
    }
  });
