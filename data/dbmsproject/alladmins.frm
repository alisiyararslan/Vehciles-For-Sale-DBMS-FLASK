TYPE=VIEW
query=select `dbmsproject`.`logs`.`id` AS `id`,`dbmsproject`.`logs`.`type` AS `type`,`dbmsproject`.`logs`.`date` AS `date`,`dbmsproject`.`logs`.`user_id` AS `user_id`,`dbmsproject`.`users`.`username` AS `username` from (`dbmsproject`.`logs` join `dbmsproject`.`users` on(`dbmsproject`.`logs`.`user_id` = `dbmsproject`.`users`.`id`)) order by `dbmsproject`.`logs`.`date` desc
md5=848aa3b6d72df9db2389062e88815de9
updatable=1
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=2022-12-18 22:25:13
create-version=2
source=SELECT logs.id ,logs.type,logs.date,logs.user_id,users.username   FROM logs\n    INNER JOIN users\n    ON logs.user_id=users.id\n    ORDER BY logs.date DESC
client_cs_name=utf8
connection_cl_name=utf8_general_ci
view_body_utf8=select `dbmsproject`.`logs`.`id` AS `id`,`dbmsproject`.`logs`.`type` AS `type`,`dbmsproject`.`logs`.`date` AS `date`,`dbmsproject`.`logs`.`user_id` AS `user_id`,`dbmsproject`.`users`.`username` AS `username` from (`dbmsproject`.`logs` join `dbmsproject`.`users` on(`dbmsproject`.`logs`.`user_id` = `dbmsproject`.`users`.`id`)) order by `dbmsproject`.`logs`.`date` desc
mariadb-version=100424
