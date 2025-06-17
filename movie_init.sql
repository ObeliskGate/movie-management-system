CREATE DATABASE IF NOT EXISTS movie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movie_db;


-- 创建表
CREATE TABLE production_company (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    city VARCHAR(20)
);

CREATE TABLE director_info (
    director_id INT PRIMARY KEY,
    director_name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    country VARCHAR(20)
);

CREATE TABLE movie_info (
    movie_id INT PRIMARY KEY,
    movie_name VARCHAR(50) NOT NULL,
    release_date DATE,
    country VARCHAR(20),
    type VARCHAR(20),
    year INT,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES production_company(company_id)
);

CREATE TABLE actor_info (
    actor_id INT PRIMARY KEY,
    actor_name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    country VARCHAR(20)
);

CREATE TABLE role_info (
    role_id INT PRIMARY KEY,
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor_info(actor_id),
    UNIQUE (movie_id, actor_id)
);

CREATE TABLE movie_director_relation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id),
    FOREIGN KEY (director_id) REFERENCES director_info(director_id),
    UNIQUE (movie_id, director_id)
);

-- 插入示例数据
INSERT INTO production_company (company_id, company_name, city) VALUES
(4001, '北京文化', '北京'),
(4002, '光线传媒', '北京'),
(4003, '中影集团', '北京'),
(4004, '华谊兄弟', '上海'),
(4005, '迪士尼', '洛杉矶');

INSERT INTO director_info (director_id, director_name, gender, country) VALUES
(3001, '吴京', '男', '中国'),
(3002, '饺子', '男', '中国'),
(3003, '郭帆', '男', '中国'),
(3004, '罗素兄弟', '男', '美国'),
(3005, '林超贤', '男', '中国');

INSERT INTO movie_info (movie_id, movie_name, release_date, country, type, year, company_id) VALUES
(1001, '战狼2', '2017-07-27', '中国', '战争', 2017, 4001),
(1002, '哪吒之魔童降世', '2019-07-26', '中国', '动画', 2019, 4002),
(1003, '流浪地球', '2019-02-05', '中国', '科幻', 2019, 4003),
(1004, '复仇者联盟4', '2019-04-24', '美国', '科幻', 2019, 4005),
(1005, '红海行动', '2018-02-16', '中国', '战争', 2018, 4004);

INSERT INTO actor_info (actor_id, actor_name, gender, country) VALUES
(2001, '吴京', '男', '中国'),
(2002, '屈楚萧', '男', '中国'),
(2003, '张译', '男', '中国'),
(2004, '小罗伯特·唐尼', '男', '美国'),
(2005, '克里斯·埃文斯', '男', '美国');

INSERT INTO role_info (role_id, movie_id, actor_id, role_name) VALUES
(5001, 1001, 2001, '冷锋'),
(5002, 1003, 2002, '刘启'),
(5003, 1003, 2003, '王磊'),
(5004, 1004, 2004, '钢铁侠'),
(5005, 1004, 2005, '美国队长');

INSERT INTO movie_director_relation (movie_id, director_id) VALUES
(1001, 3001),
(1002, 3002),
(1003, 3003),
(1004, 3004),
(1005, 3005);