<!DOCTYPE html>
<html>
<head>
    <title> Welcome to DevOps on AWS</title>
</head>
<body>
    <?php
        require 'Welcome.php';
        $welcome = new Welcome();
    ?>
    <h1><?php echo $welcome->greet()?></h1>
    <h2> Check the CI/CD with Jenkins, CodeDeploy and Code Pipeline</h2>
</body>
</html>
