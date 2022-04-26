var script1 = document.createElement('script');
script1.type = 'text/javascript';
script1.src = 'https://cdn.rawgit.com/ricmoo/aes-js/e27b99df/index.js';
const key = aesjs.utils.utf8.toBytes("KCSC@Secret__KEY");
const iv = aesjs.utils.utf8.toBytes("KCSC@Padding__@@");
for (let i = 1; i < 1000; i++) {
    item = i.toString()
    item = item.length % 16 === 0 ? item : item.concat(Array(16 - item.length % 16).fill("\x00").join(""));
    let textBytes = aesjs.utils.utf8.toBytes(item);
    var aesCbc = new aesjs.ModeOfOperation.cbc(key, iv);
    var encryptedBytes = aesCbc.encrypt(textBytes);
    var encrypted = btoa(String.fromCharCode.apply(null, encryptedBytes));
    console.log(encrypted);
}