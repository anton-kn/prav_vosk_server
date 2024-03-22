<?php

require_once("./vendor/autoload.php");

use WebSocket\Client;

/**
 * Получаем распознанный текст и опечаток речи
 * В аудио-файле должна быть только одна речь (монолог)
 */


$client = new Client("ws://localhost:2700", array('timeout' => 2000));

$config = [
   "config" => [
       "spk" => true
   ]
];

$client->send(json_encode($config));
$myfile = fopen("sample_3.wav", "r");
$res = [];
while (!feof($myfile)) {
   $data = fread($myfile, 8000);
   $client->send($data, 'binary');
   $out = $client->receive();
   echo $out . "\n"; 
   if ($isOut = json_decode($out, true)) {
      $res[] = $isOut;
   }
}
$client->send("{\"eof\" : 1}");
$out = $client->receive();
if ($isOut = json_decode($out, true)) {
   $res[] = $isOut;
}
echo $out . "\n";

fclose($myfile);

var_dump($res);

function jsonDecode($data)
{
   $values = json_decode($data, true);
   if($values){
      return $values;
   }
}
