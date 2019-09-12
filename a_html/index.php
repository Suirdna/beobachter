<?php
$servername = "localhost";
$username = "admin";
$password = "";
$dbname = "beobachter_tabelle";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if ($conn === false) {
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "SELECT * FROM allgemein_statistik ORDER BY zahl DESC";
?>
<!doctype html>
<html lang="lt">
<head>
    <title>Beobachter - Statistika</title>
    <link rel="stylesheet" type="text/css" href="./style/style.css"/>
    <link rel="shortcut icon" type="image/png" href="./favicon.ico"/>
    <meta name="view-port" content="width=device-with, initial-scale=1.0"/>
    <meta charset="UTF-8"/>
    <meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1"> 
</head>
<body>
    <div class="wrapper">
        <header>
            <div class="control"></div>
            <div class="logo">
                <div class="image"></div>
            </div>
            <div class="join"><a href="https://discord.gg/TWzT52F"></a></div>
        </header>
        <main>
            <table id="statistic" class="display" style="width:100%">
        <thead>
            <tr>
                <th>VIETA</th>
                <th>SERVERIS</th>
                <th>RSN</th>
                <th>UŽDARBIS</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $count = 0;
            if($result = mysqli_query($conn, $sql)){
                if(mysqli_num_rows($result) > 0){
                    while($row = mysqli_fetch_array($result)){
                        if (strcmp($row["benutzer_name"],'random')!=0){
                            $count++;
                            $number = $row["zahl"];
                            $sum = number_format($number);

                            $username = str_replace('?','&#9876', $row["benutzer_name"]);
                            echo "<tr>";
                                echo "<th>".$count;
                                echo "<th>".$row["kanal_name"];
                                echo "<th>".$username;
                                echo "<th>".$sum."<img src='./images/gp.png'/>";
                            echo "</tr>"; 
                        }else{
                            
                        }  
                    }
                   mysqli_free_result($result); 
                }else{
                    echo "";
                }
            }else{
                echo "";
            }
            ?>
        </tbody>
            </table>
        </main>
        <footer>
        </footer>
    </div>
</body>
</html>