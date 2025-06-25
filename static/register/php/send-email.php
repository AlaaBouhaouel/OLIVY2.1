<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    // Replace this with your own email address
    $to = 'ellabouhawel@gmail.com';

    // Validate and sanitize form data
    $name = isset($_POST['name']) ? trim($_POST['name']) : '';
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $contact_message = isset($_POST['message']) ? trim($_POST['message']) : '';

    // Validate email format
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "Invalid email address. Please provide a valid email.";
        exit;
    }

    // Set default subject if not provided
    $subject = isset($_POST['subject']) ? trim($_POST['subject']) : "Contact Form Submission";

    // Set Message
    $message = "Email from: " . $name . "\r\n";
    $message .= "Email address: " . $email . "\r\n";
    $message .= "Message: \r\n";
    $message .= $contact_message . "\r\n";
    $message .= "-----\r\nThis email was sent from your site " . url() . " contact form.\r\n";

    // Set From: header
    $from =  $name . " <" . $email . ">";

    // Email Headers
    $headers = "From: " . $from . "\r\n";
    $headers .= "Reply-To: " . $email . "\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=ISO-8859-1\r\n";

    // Send email
    if (mail($to, $subject, $message, $headers)) {
        echo "OK";
    } else {
        echo "Something went wrong. Please try again.";
    }
}
?>
