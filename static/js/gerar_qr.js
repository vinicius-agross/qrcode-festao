// qrcode-generator.js

// Certifique-se de que o elemento com id="qrcode" existe no HTML
var qrcode = new QRCode(document.getElementById("qrcode"), {
  width: 100,
  height: 100,
});

function makeCode() {
  var elText = document.getElementsByName("codigo");

  if (!elText.value) {
    alert("Input a text");
    elText.focus();
    return;
  }

  qrcode.makeCode(elText.value);
}

makeCode();

$("#codigo")
  .on("blur", function () {
    makeCode();
  })
  .on("keydown", function (e) {
    if (e.keyCode == 13) {
      makeCode();
    }
  });
