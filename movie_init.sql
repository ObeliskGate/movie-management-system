CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;
-- 创建出品公司表
CREATE TABLE IF NOT EXISTS production_company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    city VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建演员表
CREATE TABLE IF NOT EXISTS actor_info (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    actor_name VARCHAR(50) NOT NULL,
    gender VARCHAR(2) NOT NULL,
    country VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建导演表
CREATE TABLE IF NOT EXISTS director_info (
    director_id INT AUTO_INCREMENT PRIMARY KEY,
    director_name VARCHAR(50) NOT NULL,
    gender VARCHAR(2) NOT NULL,
    country VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建电影表
CREATE TABLE IF NOT EXISTS movie_info (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(50) NOT NULL,
    release_date DATE,
    country VARCHAR(20),
    type VARCHAR(20),
    year INT,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES production_company(company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建角色表
CREATE TABLE IF NOT EXISTS role_info (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor_info(actor_id),
    UNIQUE (movie_id, actor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建演员-电影关系表
CREATE TABLE IF NOT EXISTS actor_movie_relation (
    actor_id INT NOT NULL,
    movie_id INT NOT NULL,
    PRIMARY KEY (actor_id, movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor_info(actor_id),
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建导演-电影关系表
CREATE TABLE IF NOT EXISTS director_movie_relation (
    director_id INT NOT NULL,
    movie_id INT NOT NULL,
    PRIMARY KEY (director_id, movie_id),
    FOREIGN KEY (director_id) REFERENCES director_info(director_id),
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入出品公司数据
INSERT INTO production_company (company_name, city) VALUES
('华谊兄弟', '北京'),
('光线传媒', '北京'),
('博纳影业', '深圳'),
('万达影视', '大连'),
('阿里影业', '杭州');

-- 插入演员数据
INSERT INTO actor_info (actor_name, gender, country) VALUES
('吴京', '男', '中国'),
('沈腾', '男', '中国'),
('张译', '男', '中国'),
('周冬雨', '女', '中国'),
('章子怡', '女', '中国'),
('黄渤', '男', '中国'),
('徐峥', '男', '中国'),
('王宝强', '男', '中国'),
('邓超', '男', '中国'),
('刘昊然', '男', '中国');

-- 插入导演数据
INSERT INTO director_info (director_name, gender, country) VALUES
('张艺谋', '男', '中国'),
('陈凯歌', '男', '中国'),
('冯小刚', '男', '中国'),
('宁浩', '男', '中国'),
('徐克', '男', '中国'),
('管虎', '男', '中国'),
('贾樟柯', '男', '中国'),
('文牧野', '男', '中国');

-- 插入电影数据
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
('战狼2', '2017-07-27', '中国', '动作', 2017, 1),
('流浪地球', '2019-02-05', '中国', '科幻', 2019, 2),
('你好，李焕英', '2021-02-12', '中国', '喜剧', 2021, 3),
('长津湖', '2021-09-30', '中国', '战争', 2021, 4),
('哪吒之魔童降世', '2019-07-26', '中国', '动画', 2019, 5),
('红海行动', '2018-02-16', '中国', '动作', 2018, 1),
('我不是药神', '2018-07-05', '中国', '剧情', 2018, 2),
('唐人街探案3', '2021-02-12', '中国', '喜剧', 2021, 3),
('我和我的祖国', '2019-09-30', '中国', '剧情', 2019, 4),
('八佰', '2020-08-21', '中国', '战争', 2020, 5);

-- 插入演员-电影关系
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
(1, 1), (1, 2), (1, 4),  -- 吴京
(2, 3), (2, 8),          -- 沈腾
(3, 4), (3, 6), (3, 9),  -- 张译
(4, 3), (4, 9),          -- 周冬雨
(5, 9),                  -- 章子怡
(6, 7), (6, 8),          -- 黄渤
(7, 7), (7, 8),          -- 徐峥
(8, 6), (8, 8),          -- 王宝强
(9, 8), (9, 9),          -- 邓超
(10, 2), (10, 8);        -- 刘昊然

-- 插入导演-电影关系
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(1, 9),                  -- 张艺谋
(2, 4),                  -- 陈凯歌
(3, 1),                  -- 冯小刚
(4, 3), (4, 7),          -- 宁浩
(5, 2),                  -- 徐克
(6, 4), (6, 10),         -- 管虎
(8, 7);                  -- 文牧野

-- 插入角色数据
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
(1, 1, '冷锋'),
(2, 1, '刘培强'),
(2, 10, '刘启'),
(3, 2, '贾晓玲'),
(3, 4, '李焕英（青年）'),
(4, 1, '伍千里'),
(4, 3, '梅生'),
(6, 3, '杨锐'),
(6, 8, '李懂'),
(7, 6, '程勇');