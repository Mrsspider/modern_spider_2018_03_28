
level1, level2, level3, name, p_br, p_name, p_price, old_price, product_url, img

create database modern charset=utf8;

use modern;

create table modern_product(
id int not null auto_increment,
level1 varchar(20) default null,
level2 varchar(20) default null,
level3 varchar(20) default null,
level4 varchar(20) default null,
p_br varchar(40) default null,
p_name varchar(148) default null,
p_price int(7) default null,
old_price int(7) default null,
product_url varchar(48) default null,
img varchar(148) default null,
createtime datetime DEFAULT CURRENT_TIMESTAMP,
updatetime datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
primary key(id)
) charset=utf8;

create table p_c_z(
id int not null auto_increment,
c_z varchar(148) default null,
p_id int,
primary key(id),
foreign key(p_id) references modern_product(id)
) charset=utf8;

select * from p_c_z join (select id,p_name,p_br,p_price,old_price from modern_product where level4='衬衫') t1 where t1.id=p_id;