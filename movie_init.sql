CREATE DATABASE IF NOT EXISTS movie_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE movie_db;

-- 创建出品公司表
CREATE TABLE IF NOT EXISTS production_company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    city VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建演员表 (修改点：将gender改为type)
CREATE TABLE IF NOT EXISTS actor_info (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    actor_name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,  -- 修改点：gender改为type
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

-- 1. 创建出品公司表数据（从ID 1开始）
INSERT INTO production_company (company_name, city) VALUES
('派拉蒙影业', '洛杉矶'),      -- company_id 1
('华纳兄弟', '伯班克'),        -- company_id 2
('环球影业', '环球城'),        -- company_id 3
('新线影业', '洛杉矶'),        -- company_id 4
('米拉麦克斯', '洛杉矶'),      -- company_id 5
('Gaumont', '巴黎'),          -- company_id 6
('Orion Pictures', '纽约'),   -- company_id 7
('Melampo', '罗马');          -- company_id 8

-- 2. 创建导演表数据（从ID 1开始）
INSERT INTO director_info (director_name, gender, country) VALUES
('弗兰克·德拉邦特', '男', '美国'),       -- director_id 1
('弗朗西斯·福特·科波拉', '男', '美国'),  -- director_id 2
('克里斯托弗·诺兰', '男', '英国'),       -- director_id 3
('史蒂文·斯皮尔伯格', '男', '美国'),     -- director_id 4
('彼得·杰克逊', '男', '新西兰'),         -- director_id 5
('昆汀·塔伦蒂诺', '男', '美国'),         -- director_id 6
('大卫·芬奇', '男', '美国'),             -- director_id 7
('吕克·贝松', '男', '法国'),             -- director_id 8
('乔纳森·戴米', '男', '美国'),           -- director_id 9
('罗伯托·贝尼尼', '男', '意大利');       -- director_id 10

-- 3. 创建演员表数据（从ID 1开始）
INSERT INTO actor_info (actor_name, type, country) VALUES
('蒂姆·罗宾斯', '男', '美国'),           -- actor_id 1
('摩根·弗里曼', '男', '美国'),           -- actor_id 2
('马龙·白兰度', '男', '美国'),           -- actor_id 3
('阿尔·帕西诺', '男', '美国'),           -- actor_id 4
('克里斯蒂安·贝尔', '男', '英国'),       -- actor_id 5
('希斯·莱杰', '男', '澳大利亚'),         -- actor_id 6
('连姆·尼森', '男', '英国'),             -- actor_id 7
('伊利亚·伍德', '男', '美国'),           -- actor_id 8
('约翰·特拉沃尔塔', '男', '美国'),       -- actor_id 9
('乌玛·瑟曼', '女', '美国'),             -- actor_id 10
('爱德华·诺顿', '男', '美国'),           -- actor_id 11
('布拉德·皮特', '男', '美国'),           -- actor_id 12
('让·雷诺', '男', '法国'),               -- actor_id 13
('娜塔莉·波特曼', '女', '美国'),         -- actor_id 14
('安东尼·霍普金斯', '男', '英国'),       -- actor_id 15
('朱迪·福斯特', '女', '美国'),           -- actor_id 16
('罗伯托·贝尼尼', '男', '意大利'),       -- actor_id 17
('尼可莱塔·布拉斯基', '女', '意大利');   -- actor_id 18

-- 4. 创建电影表数据（从ID 1开始）
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
('肖申克的救赎', '1994-09-23', '美国', '剧情', 1994, 4),    -- movie_id 1 (新线影业)
('教父', '1972-03-24', '美国', '犯罪', 1972, 1),          -- movie_id 2 (派拉蒙)
('黑暗骑士', '2008-07-18', '美国', '动作', 2008, 2),       -- movie_id 3 (华纳兄弟)
('辛德勒的名单', '1993-12-15', '美国', '历史', 1993, 3),   -- movie_id 4 (环球)
('指环王3：王者归来', '2003-12-17', '新西兰', '奇幻', 2003, 4), -- movie_id 5 (新线)
('低俗小说', '1994-10-14', '美国', '犯罪', 1994, 5),      -- movie_id 6 (米拉麦克斯)
('搏击俱乐部', '1999-10-15', '美国', '剧情', 1999, 2),     -- movie_id 7 (华纳兄弟)
('这个杀手不太冷', '1994-09-14', '法国', '犯罪', 1994, 6), -- movie_id 8 (Gaumont)
('沉默的羔羊', '1991-02-14', '美国', '惊悚', 1991, 7),    -- movie_id 9 (Orion)
('美丽人生', '1997-12-20', '意大利', '剧情', 1997, 8);   -- movie_id 10 (Melampo)

-- 5. 创建导演-电影关系
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(1, 1),   -- 肖申克的救赎 - 德拉邦特
(2, 2),   -- 教父 - 科波拉
(3, 3),   -- 黑暗骑士 - 诺兰
(4, 4),   -- 辛德勒名单 - 斯皮尔伯格
(5, 5),   -- 指环王3 - 杰克逊
(6, 6),   -- 低俗小说 - 塔伦蒂诺
(7, 7),   -- 搏击俱乐部 - 芬奇
(8, 8),   -- 这个杀手不太冷 - 贝松
(9, 9),   -- 沉默的羔羊 - 戴米
(10, 10); -- 美丽人生 - 贝尼尼

-- 6. 创建演员-电影关系
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 肖申克的救赎
(1, 1), (2, 1),
-- 教父
(3, 2), (4, 2),
-- 黑暗骑士
(5, 3), (6, 3),
-- 辛德勒名单
(7, 4),
-- 指环王3
(8, 5),
-- 低俗小说
(9, 6), (10, 6),
-- 搏击俱乐部
(11, 7), (12, 7),
-- 这个杀手不太冷
(13, 8), (14, 8),
-- 沉默的羔羊
(15, 9), (16, 9),
-- 美丽人生
(17, 10), (18, 10);

-- 7. 创建角色信息
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 肖申克的救赎
(1, 1, '安迪·杜佛兰'), 
(1, 2, '埃利斯·"瑞德"·雷丁'),
-- 教父
(2, 3, '维托·柯里昂'), 
(2, 4, '迈克尔·柯里昂'),
-- 黑暗骑士
(3, 5, '布鲁斯·韦恩/蝙蝠侠'), 
(3, 6, '小丑'),
-- 辛德勒名单
(4, 7, '奥斯卡·辛德勒'),
-- 指环王3
(5, 8, '弗罗多·巴金斯'),
-- 低俗小说
(6, 9, '文森特·维加'), 
(6, 10, '米娅·华莱士'),
-- 搏击俱乐部
(7, 11, '叙述者'), 
(7, 12, '泰勒·德顿'),
-- 这个杀手不太冷
(8, 13, '莱昂'), 
(8, 14, '玛蒂尔达'),
-- 沉默的羔羊
(9, 15, '汉尼拔·莱克特'), 
(9, 16, '克拉丽斯·史达琳'),
-- 美丽人生
(10, 17, '圭多'), 
(10, 18, '多拉');

-- 新增电影数据（ID 11-20）--
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
-- 使用已有公司ID：
('教父2', '1974-12-20', '美国', '犯罪', 1974, 1),          -- company_id 1 (派拉蒙)
('盗梦空间', '2010-07-16', '美国', '科幻', 2010, 2),       -- company_id 2 (华纳兄弟)
('侏罗纪公园', '1993-06-11', '美国', '科幻', 1993, 3),    -- company_id 3 (环球)
('指环王1：魔戒再现', '2001-12-19', '新西兰', '奇幻', 2001, 4), -- company_id 4 (新线)
('杀死比尔', '2003-10-10', '美国', '动作', 2003, 5),      -- company_id 5 (米拉麦克斯)
('第五元素', '1997-05-07', '法国', '科幻', 1997, 6),      -- company_id 6 (Gaumont)
('汉尼拔', '2001-02-09', '美国', '惊悚', 2001, 7),        -- company_id 7 (Orion)
('黑客帝国', '1999-03-31', '美国', '科幻', 1999, 2),      -- company_id 2 (华纳兄弟)
('海上钢琴师', '1998-10-28', '意大利', '剧情', 1998, 8),  -- company_id 8 (Melampo)
('七宗罪', '1995-09-22', '美国', '犯罪', 1995, 2);        -- company_id 2 (华纳兄弟)

-- 新增导演（ID 11-13）--
INSERT INTO director_info (director_name, gender, country) VALUES
('詹姆斯·卡梅隆', '男', '加拿大'),      -- director_id 11 (备用)
('沃卓斯基姐妹', '女', '美国'),         -- director_id 12
('朱塞佩·托纳多雷', '男', '意大利');    -- director_id 13

-- 新增演员（ID 19-28）--
INSERT INTO actor_info (actor_name, type, country) VALUES
('罗伯特·德尼罗', '男', '美国'),        -- actor_id 19
('艾伦·佩吉', '女', '加拿大'),          -- actor_id 20
('山姆·尼尔', '男', '新西兰'),          -- actor_id 21
('乌玛·瑟曼', '女', '美国'),            -- actor_id 22 (已有)
('布鲁斯·威利斯', '男', '美国'),        -- actor_id 23
('米拉·乔沃维奇', '女', '乌克兰'),      -- actor_id 24
('加里·奥德曼', '男', '英国'),          -- actor_id 25
('基努·里维斯', '男', '加拿大'),        -- actor_id 26
('蒂姆·罗斯', '男', '英国'),           -- actor_id 27
('凯文·史派西', '男', '美国');          -- actor_id 28

-- 导演-电影关系 --
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(2, 11),    -- 教父2 - 科波拉 (已有)
(3, 12),    -- 盗梦空间 - 诺兰 (已有)
(4, 13),    -- 侏罗纪公园 - 斯皮尔伯格 (已有)
(5, 14),    -- 指环王1 - 杰克逊 (已有)
(6, 15),    -- 杀死比尔 - 塔伦蒂诺 (已有)
(8, 16),    -- 第五元素 - 贝松 (已有)
(9, 17),    -- 汉尼拔 - 戴米 (已有)
(12, 18),   -- 黑客帝国 - 沃卓斯基
(13, 19),   -- 海上钢琴师 - 托纳多雷
(7, 20);    -- 七宗罪 - 芬奇 (已有)

-- 演员-电影关系 --
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 教父2
(4, 11), (19, 11),   -- 帕西诺, 德尼罗
-- 盗梦空间
(5, 12), (20, 12),   -- 贝尔, 佩吉
-- 侏罗纪公园
(21, 13),            -- 山姆·尼尔
-- 指环王1
(8, 14),             -- 伊利亚·伍德
-- 杀死比尔
(10, 15), (23, 15),  -- 瑟曼, 威利斯
-- 第五元素
(23, 16), (24, 16),  -- 威利斯, 乔沃维奇
-- 汉尼拔
(15, 17),            -- 霍普金斯
-- 黑客帝国
(26, 18),            -- 基努·里维斯
-- 海上钢琴师
(27, 19),            -- 蒂姆·罗斯
-- 七宗罪
(12, 20), (28, 20);  -- 皮特, 史派西

-- 角色信息 --
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 教父2
(11, 4, '迈克尔·柯里昂'), 
(11, 19, '年轻维托·柯里昂'),
-- 盗梦空间
(12, 5, '柯布'), 
(12, 20, '阿里阿德涅'),
-- 侏罗纪公园
(13, 21, '格兰特博士'),
-- 指环王1
(14, 8, '弗罗多·巴金斯'),
-- 杀死比尔
(15, 10, '新娘'), 
(15, 23, '保罗'),
-- 第五元素
(16, 23, '科本'), 
(16, 24, '丽露'),
-- 汉尼拔
(17, 15, '汉尼拔·莱克特'),
-- 黑客帝国
(18, 26, '尼奥'),
-- 海上钢琴师
(19, 27, '1900'),
-- 七宗罪
(20, 12, '米尔斯'), 
(20, 28, '约翰·杜');

-- 新增电影数据（ID 21-30）--
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
-- 复用已有公司ID：
('教父3', '1990-12-25', '美国', '犯罪', 1990, 1),          -- company_id 1 (派拉蒙)
('星际穿越', '2014-11-07', '美国', '科幻', 2014, 2),      -- company_id 2 (华纳兄弟)
('E.T.外星人', '1982-06-11', '美国', '科幻', 1982, 3),    -- company_id 3 (环球)
('指环王2：双塔奇兵', '2002-12-18', '新西兰', '奇幻', 2002, 4), -- company_id 4 (新线)
('无耻混蛋', '2009-08-21', '美国', '战争', 2009, 5),     -- company_id 5 (米拉麦克斯)
('超体', '2014-07-25', '法国', '科幻', 2014, 6),          -- company_id 6 (Gaumont)
('红龙', '2002-10-04', '美国', '惊悚', 2002, 7),           -- company_id 7 (Orion)
('黑客帝国2：重装上阵', '2003-05-15', '美国', '科幻', 2003, 2), -- company_id 2 (华纳兄弟)
('天堂电影院', '1988-11-17', '意大利', '剧情', 1988, 8),   -- company_id 8 (Melampo)
('消失的爱人', '2014-10-03', '美国', '惊悚', 2014, 2);     -- company_id 2 (华纳兄弟)

-- 新增导演（ID 14-15）--
INSERT INTO director_info (director_name, gender, country) VALUES
('雷德利·斯科特', '男', '英国'),       -- director_id 14
('大卫·芬奇', '男', '美国');           -- director_id 15 (已有，但确保ID连续)

-- 新增演员（ID 29-38）--
INSERT INTO actor_info (actor_name, type, country) VALUES
('安迪·加西亚', '男', '美国'),         -- actor_id 29
('马修·麦康纳', '男', '美国'),         -- actor_id 30
('亨利·托马斯', '男', '美国'),         -- actor_id 31
('布拉德·皮特', '男', '美国'),         -- actor_id 32 (已有)
('克里斯托弗·瓦尔兹', '男', '奥地利'), -- actor_id 33
('斯嘉丽·约翰逊', '女', '美国'),       -- actor_id 34
('爱德华·诺顿', '男', '美国'),         -- actor_id 35 (已有)
('劳伦斯·菲什伯恩', '男', '美国'),     -- actor_id 36
('菲利普·诺瓦雷', '男', '法国'),       -- actor_id 37
('本·阿弗莱克', '男', '美国');         -- actor_id 38

-- 导演-电影关系 --
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(2, 21),    -- 教父3 - 科波拉 (已有)
(3, 22),    -- 星际穿越 - 诺兰 (已有)
(4, 23),    -- E.T. - 斯皮尔伯格 (已有)
(5, 24),    -- 指环王2 - 杰克逊 (已有)
(6, 25),    -- 无耻混蛋 - 塔伦蒂诺 (已有)
(8, 26),    -- 超体 - 贝松 (已有)
(9, 27),    -- 红龙 - 戴米 (已有)
(12, 28),   -- 黑客帝国2 - 沃卓斯基 (已有)
(13, 29),   -- 天堂电影院 - 托纳多雷 (已有)
(15, 30);   -- 消失的爱人 - 芬奇 (已有)

-- 演员-电影关系 --
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 教父3
(4, 21), (29, 21),   -- 帕西诺, 加西亚
-- 星际穿越
(30, 22),            -- 麦康纳
-- E.T.外星人
(31, 23),            -- 托马斯
-- 指环王2
(8, 24),             -- 伊利亚·伍德
-- 无耻混蛋
(32, 25), (33, 25),  -- 皮特, 瓦尔兹
-- 超体
(34, 26),            -- 约翰逊
-- 红龙
(35, 27),            -- 诺顿
-- 黑客帝国2
(26, 28), (36, 28),  -- 里维斯, 菲什伯恩
-- 天堂电影院
(37, 29),            -- 诺瓦雷
-- 消失的爱人
(38, 30);            -- 阿弗莱克

-- 角色信息 --
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 教父3
(21, 4, '迈克尔·柯里昂'), 
(21, 29, '文森·曼西尼'),
-- 星际穿越
(22, 30, '库珀'),
-- E.T.外星人
(23, 31, '艾略特'),
-- 指环王2
(24, 8, '弗罗多·巴金斯'),
-- 无耻混蛋
(25, 32, '阿尔多·雷恩'), 
(25, 33, '汉斯·兰达'),
-- 超体
(26, 34, '露西'),
-- 红龙
(27, 35, '威尔·格雷厄姆'),
-- 黑客帝国2
(28, 26, '尼奥'), 
(28, 36, '墨菲斯'),
-- 天堂电影院
(29, 37, '阿尔弗雷多'),
-- 消失的爱人
(30, 38, '尼克·邓恩');

-- 新增出品公司（ID 9-12）--
INSERT INTO production_company (company_name, city) VALUES
('迪士尼', '伯班克'),                  -- company_id 9
('索尼影业', '卡尔弗城'),               -- company_id 10
('传奇影业', '伯班克'),                 -- company_id 11
('焦点影业', '洛杉矶');                 -- company_id 12

-- 新增导演（ID 16-20）--
INSERT INTO director_info (director_name, gender, country) VALUES
('詹姆斯·卡梅隆', '男', '加拿大'),      -- director_id 16
('吉尔莫·德尔·托罗', '男', '墨西哥'),   -- director_id 17
('丹尼斯·维伦纽夫', '男', '加拿大'),    -- director_id 18
('达伦·阿罗诺夫斯基', '男', '美国'),    -- director_id 19
('亚历杭德罗·冈萨雷斯·伊纳里图', '男', '墨西哥'); -- director_id 20

-- 新增演员（ID 39-58）--
INSERT INTO actor_info (actor_name, type, country) VALUES
('汤姆·克鲁斯', '男', '美国'),          -- actor_id 39
('汤姆·汉克斯', '男', '美国'),          -- actor_id 40
('威尔·史密斯', '男', '美国'),         -- actor_id 41
('莱昂纳多·迪卡普里奥', '男', '美国'),  -- actor_id 42
('查理兹·塞隆', '女', '南非'),          -- actor_id 43
('艾玛·沃森', '女', '英国'),            -- actor_id 44
('丹尼尔·雷德克里夫', '男', '英国'),    -- actor_id 45
('鲁伯特·格林特', '男', '英国'),        -- actor_id 46
('休·杰克曼', '男', '澳大利亚'),        -- actor_id 47
('杰克·吉伦哈尔', '男', '美国'),        -- actor_id 48
('瑞恩·高斯林', '男', '加拿大'),        -- actor_id 49
('艾米·亚当斯', '女', '美国'),          -- actor_id 50
('本尼迪克特·康伯巴奇', '男', '英国'), -- actor_id 51
('克里斯·海姆斯沃斯', '男', '澳大利亚'),-- actor_id 52
('小罗伯特·唐尼', '男', '美国'),        -- actor_id 53
('马克·鲁弗洛', '男', '美国'),          -- actor_id 54
('克里斯·埃文斯', '男', '美国'),        -- actor_id 55
('斯嘉丽·约翰逊', '女', '美国'),        -- actor_id 56 (已有)
('娜塔莉·波特曼', '女', '美国'),        -- actor_id 57 (已有)
('克里斯蒂安·贝尔', '男', '英国');      -- actor_id 58 (已有)

-- 新增电影（ID 31-50）--
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
-- 复用已有公司
('泰坦尼克号', '1997-11-18', '美国', '爱情', 1997, 1),       -- company_id 1 (派拉蒙)
('蝙蝠侠：黑暗骑士崛起', '2012-07-20', '美国', '动作', 2012, 2), -- company_id 2 (华纳)
('侏罗纪世界', '2015-06-10', '美国', '科幻', 2015, 3),       -- company_id 3 (环球)
('霍比特人1：意外之旅', '2012-12-14', '新西兰', '奇幻', 2012, 4), -- company_id 4 (新线)
('被解救的姜戈', '2012-12-25', '美国', '西部', 2012, 5),     -- company_id 5 (米拉麦克斯)
-- 使用新公司
('阿凡达', '2009-12-18', '美国', '科幻', 2009, 9),           -- company_id 9 (迪士尼)
('水形物语', '2017-12-01', '美国', '奇幻', 2017, 10),        -- company_id 10 (索尼)
('银翼杀手2049', '2017-10-06', '美国', '科幻', 2017, 11),    -- company_id 11 (传奇)
('黑天鹅', '2010-12-03', '美国', '心理', 2010, 12),          -- company_id 12 (焦点)
('荒野猎人', '2015-12-16', '美国', '冒险', 2015, 1),         -- company_id 1 (派拉蒙)
-- 系列电影保持同公司
('黑客帝国3：矩阵革命', '2003-11-05', '美国', '科幻', 2003, 2), -- company_id 2 (华纳)
('哈利·波特与魔法石', '2001-11-16', '英国', '奇幻', 2001, 2), -- company_id 2 (华纳)
('钢铁侠', '2008-05-02', '美国', '动作', 2008, 9),          -- company_id 9 (迪士尼)
('雷神', '2011-05-06', '美国', '奇幻', 2011, 9),             -- company_id 9 (迪士尼)
('美国队长', '2011-07-22', '美国', '动作', 2011, 9),         -- company_id 9 (迪士尼)
('复仇者联盟', '2012-05-04', '美国', '动作', 2012, 9),       -- company_id 9 (迪士尼)
('星际迷航', '2009-05-08', '美国', '科幻', 2009, 1),         -- company_id 1 (派拉蒙)
('变形金刚', '2007-07-03', '美国', '科幻', 2007, 3),         -- company_id 3 (环球)
('速度与激情7', '2015-04-03', '美国', '动作', 2015, 3),      -- company_id 3 (环球)
('加勒比海盗', '2003-07-09', '美国', '冒险', 2003, 9);       -- company_id 9 (迪士尼)

-- 导演-电影关系 --
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
-- 复用已有导演
(16, 31),   -- 泰坦尼克号 - 卡梅隆
(3, 32),    -- 黑暗骑士崛起 - 诺兰
(4, 33),    -- 侏罗纪世界 - 斯皮尔伯格
(5, 34),    -- 霍比特人1 - 杰克逊
(6, 35),    -- 被解救的姜戈 - 塔伦蒂诺
-- 新导演
(16, 36),   -- 阿凡达 - 卡梅隆
(17, 37),   -- 水形物语 - 德尔·托罗
(18, 38),   -- 银翼杀手2049 - 维伦纽夫
(19, 39),   -- 黑天鹅 - 阿罗诺夫斯基
(20, 40),   -- 荒野猎人 - 伊纳里图
-- 系列导演
(12, 41),   -- 黑客帝国3 - 沃卓斯基
(14, 42),   -- 哈利波特1 - 克里斯·哥伦布(新增需补)
(15, 43),   -- 钢铁侠 - 乔恩·费儒(新增需补)
(14, 44),   -- 雷神 - 肯尼思·布拉纳(新增需补)
(14, 45),   -- 美国队长 - 乔·庄斯顿(新增需补)
(14, 46),   -- 复仇者联盟 - 乔斯·韦登(新增需补)
(3, 47),    -- 星际迷航 - J·J·艾布拉姆斯(新增需补)
(14, 48),   -- 变形金刚 - 迈克尔·贝(新增需补)
(14, 49),   -- 速度与激情7 - 温子仁(新增需补)
(14, 50);   -- 加勒比海盗 - 戈尔·维宾斯基(新增需补)

-- 补充新增导演 --
INSERT INTO director_info (director_name, gender, country) VALUES
('克里斯·哥伦布', '男', '美国'),       -- director_id 21
('乔恩·费儒', '男', '美国'),           -- director_id 22
('肯尼思·布拉纳', '男', '英国'),       -- director_id 23
('乔·庄斯顿', '男', '美国'),           -- director_id 24
('乔斯·韦登', '男', '美国'),           -- director_id 25
('J·J·艾布拉姆斯', '男', '美国'),      -- director_id 26
('迈克尔·贝', '男', '美国'),           -- director_id 27
('温子仁', '男', '澳大利亚'),           -- director_id 28
('戈尔·维宾斯基', '男', '美国');       -- director_id 29

-- 更新导演-电影关系 --
UPDATE director_movie_relation SET director_id = 21 WHERE movie_id = 42; -- 哈利波特
UPDATE director_movie_relation SET director_id = 22 WHERE movie_id = 43; -- 钢铁侠
UPDATE director_movie_relation SET director_id = 23 WHERE movie_id = 44; -- 雷神
UPDATE director_movie_relation SET director_id = 24 WHERE movie_id = 45; -- 美队
UPDATE director_movie_relation SET director_id = 25 WHERE movie_id = 46; -- 复联
UPDATE director_movie_relation SET director_id = 26 WHERE movie_id = 47; -- 星际迷航
UPDATE director_movie_relation SET director_id = 27 WHERE movie_id = 48; -- 变形金刚
UPDATE director_movie_relation SET director_id = 28 WHERE movie_id = 49; -- 速激7
UPDATE director_movie_relation SET director_id = 29 WHERE movie_id = 50; -- 加勒比

-- 演员-电影关系 --
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 泰坦尼克号
(42, 31), (43, 31),   -- 迪卡普里奥, 温斯莱特(需补)
-- 黑暗骑士崛起
(58, 32),             -- 贝尔
-- 侏罗纪世界
(39, 33),             -- 克鲁斯
-- 霍比特人1
(8, 34),              -- 伊利亚·伍德
-- 被解救的姜戈
(42, 35), (33, 35),   -- 迪卡普里奥, 瓦尔兹
-- 阿凡达
(42, 36),             -- 迪卡普里奥(应为萨姆·沃辛顿，需补)
-- 水形物语
(50, 37),             -- 亚当斯
-- 银翼杀手2049
(49, 38),             -- 高斯林
-- 黑天鹅
(57, 39),             -- 波特曼
-- 荒野猎人
(42, 40),             -- 迪卡普里奥
-- 黑客帝国3
(26, 41), (36, 41),   -- 里维斯, 菲什伯恩
-- 哈利波特1
(44, 42), (45, 42), (46, 42), -- 沃森, 雷德克里夫, 格林特
-- 钢铁侠
(53, 43),             -- 唐尼
-- 雷神
(52, 44),             -- 海姆斯沃斯
-- 美国队长
(55, 45),             -- 埃文斯
-- 复仇者联盟
(53, 46), (52, 46), (55, 46), (56, 46), -- 唐尼, 海姆斯沃斯, 埃文斯, 约翰逊
-- 星际迷航
(39, 47),             -- 克鲁斯
-- 变形金刚
(41, 48),             -- 史密斯
-- 速度与激情7
(39, 49),             -- 克鲁斯
-- 加勒比海盗
(47, 50);             -- 德普(需补)

-- 补充演员 --
INSERT INTO actor_info (actor_name, type, country) VALUES
('凯特·温斯莱特', '女', '英国'),      -- actor_id 59
('萨姆·沃辛顿', '男', '澳大利亚'),     -- actor_id 60
('约翰尼·德普', '男', '美国');        -- actor_id 61

-- 更新演员-电影关系 --
UPDATE actor_movie_relation SET actor_id = 59 WHERE movie_id = 31 AND actor_id = 43; -- 泰坦尼克号女主
UPDATE actor_movie_relation SET actor_id = 60 WHERE movie_id = 36; -- 阿凡达男主
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES (61, 50); -- 加勒比海盗德普

-- 角色信息 --
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 泰坦尼克号
(31, 42, '杰克·道森'), (31, 59, '萝丝·德威特·布克特'),
-- 黑暗骑士崛起
(32, 58, '布鲁斯·韦恩/蝙蝠侠'),
-- 被解救的姜戈
(35, 42, '卡尔文·坎迪'), (35, 33, '金·舒尔茨'),
-- 哈利波特1
(42, 44, '赫敏·格兰杰'), (42, 45, '哈利·波特'), (42, 46, '罗恩·韦斯莱'),
-- 钢铁侠
(43, 53, '托尼·斯塔克/钢铁侠'),
-- 复仇者联盟
(46, 53, '钢铁侠'), (46, 52, '雷神'), (46, 55, '美国队长'), (46, 56, '黑寡妇'),
-- 加勒比海盗
(50, 61, '杰克·斯派洛');

-- 新增电影数据（ID 51-60）--
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
('阿凡达2：水之道', '2022-12-16', '美国', '科幻', 2022, 9),          -- company_id 9 (迪士尼)
('奥本海默', '2023-07-21', '美国', '传记', 2023, 3),               -- company_id 3 (环球)
('沙丘', '2021-10-22', '美国', '科幻', 2021, 11),                  -- company_id 11 (传奇)
('寄生虫', '2019-05-21', '韩国', '剧情', 2019, 12),                -- company_id 12 (焦点)
('小丑', '2019-10-04', '美国', '犯罪', 2019, 2),                   -- company_id 2 (华纳)
('哈利·波特与死亡圣器(下)', '2011-07-15', '英国', '奇幻', 2011, 2), -- company_id 2 (华纳)
('复仇者联盟4：终局之战', '2019-04-26', '美国', '动作', 2019, 9),   -- company_id 9 (迪士尼)
('壮志凌云2：独行侠', '2022-05-27', '美国', '动作', 2022, 1),       -- company_id 1 (派拉蒙)
('瞬息全宇宙', '2022-03-25', '美国', '科幻', 2022, 5),              -- company_id 5 (米拉麦克斯)
('芭比', '2023-07-21', '美国', '喜剧', 2023, 2);                    -- company_id 2 (华纳)

-- 新增导演（ID 30-32）--
INSERT INTO director_info (director_name, gender, country) VALUES
('奉俊昊', '男', '韩国'),                  -- director_id 30
('托德·菲利普斯', '男', '美国'),           -- director_id 31
('关家永', '男', '美国');                   -- director_id 32

-- 新增演员（ID 62-71）--
INSERT INTO actor_info (actor_name, type, country) VALUES
('佐伊·索尔达娜', '女', '美国'),           -- actor_id 62
('基里安·墨菲', '男', '爱尔兰'),           -- actor_id 63
('提莫西·查拉梅', '男', '美国'),           -- actor_id 64
('宋康昊', '男', '韩国'),                   -- actor_id 65
('华金·菲尼克斯', '男', '美国'),            -- actor_id 66
('丹尼尔·拉德克利夫', '男', '英国'),        -- actor_id 67 (已有)
('克里斯·埃文斯', '男', '美国'),            -- actor_id 68 (已有)
('汤姆·克鲁斯', '男', '美国'),              -- actor_id 69 (已有)
('杨紫琼', '女', '马来西亚'),               -- actor_id 70
('玛格特·罗比', '女', '澳大利亚');           -- actor_id 71

-- 导演-电影关系 --
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(16, 51),    -- 阿凡达2 - 卡梅隆
(3, 52),     -- 奥本海默 - 诺兰
(18, 53),    -- 沙丘 - 维伦纽夫
(30, 54),    -- 寄生虫 - 奉俊昊
(31, 55),    -- 小丑 - 菲利普斯
(21, 56),    -- 哈利波特7下 - 哥伦布
(25, 57),    -- 复联4 - 韦登
(26, 58),    -- 壮志凌云2 - 艾布拉姆斯
(32, 59),    -- 瞬息全宇宙 - 关家永
(27, 60);    -- 芭比 - 格蕾塔·葛韦格(需补)

-- 补充导演 --
INSERT INTO director_info (director_name, gender, country) VALUES
('格蕾塔·葛韦格', '女', '美国');           -- director_id 33

-- 更新导演-电影关系 --
UPDATE director_movie_relation SET director_id = 33 WHERE movie_id = 60;

-- 演员-电影关系 --
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 阿凡达2
(60, 51), (62, 51),   -- 沃辛顿, 索尔达娜
-- 奥本海默
(63, 52),             -- 墨菲
-- 沙丘
(64, 53),             -- 查拉梅
-- 寄生虫
(65, 54),             -- 宋康昊
-- 小丑
(66, 55),             -- 菲尼克斯
-- 哈利波特7下
(44, 56), (45, 56), (46, 56), -- 沃森, 雷德克里夫, 格林特
-- 复联4
(53, 57), (52, 57), (55, 57), (56, 57), -- 唐尼, 海姆斯沃斯, 埃文斯, 约翰逊
-- 壮志凌云2
(39, 58),             -- 克鲁斯
-- 瞬息全宇宙
(70, 59),             -- 杨紫琼
-- 芭比
(71, 60);             -- 罗比

-- 角色信息 --
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 阿凡达2
(51, 60, '杰克·萨利'), (51, 62, '涅提妮'),
-- 奥本海默
(52, 63, '罗伯特·奥本海默'),
-- 沙丘
(53, 64, '保罗·厄崔迪'),
-- 寄生虫
(54, 65, '金基泽'),
-- 小丑
(55, 66, '亚瑟·弗莱克/小丑'),
-- 哈利波特7下
(56, 44, '赫敏·格兰杰'), (56, 45, '哈利·波特'), (56, 46, '罗恩·韦斯莱'),
-- 复联4
(57, 53, '钢铁侠'), (57, 52, '雷神'), (57, 55, '美国队长'), (57, 56, '黑寡妇'),
-- 壮志凌云2
(58, 39, '皮特·"独行侠"·米切尔'),
-- 瞬息全宇宙
(59, 70, '伊芙琳·王'),
-- 芭比
(60, 71, '芭比');

-- 新增电影数据（ID 61-70）--
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
('蜘蛛侠：纵横宇宙', '2023-06-02', '美国', '动画', 2023, 10),          -- company_id 10 (索尼)
('银河护卫队3', '2023-05-05', '美国', '科幻', 2023, 9),               -- company_id 9 (迪士尼)
('奥本海默', '2023-07-21', '美国', '传记', 2023, 3),                  -- company_id 3 (环球)
('疾速追杀4', '2023-03-24', '美国', '动作', 2023, 2),                 -- company_id 2 (华纳)
('铃芽之旅', '2022-11-11', '日本', '动画', 2022, 6),                  -- company_id 6 (Gaumont)
('蚁人3：量子狂潮', '2023-02-17', '美国', '科幻', 2023, 9),           -- company_id 9 (迪士尼)
('闪电侠', '2023-06-16', '美国', '动作', 2023, 2),                    -- company_id 2 (华纳)
('流浪地球2', '2023-01-22', '中国', '科幻', 2023, 11),                -- company_id 11 (传奇)
('灌篮高手', '2022-12-03', '日本', '动画', 2022, 12),                 -- company_id 12 (焦点)
('拿破仑', '2023-11-22', '美国', '历史', 2023, 1);                    -- company_id 1 (派拉蒙)

-- 新增导演（ID 34-37）--
INSERT INTO director_info (director_name, gender, country) VALUES
('新海诚', '男', '日本'),                     -- director_id 34
('郭帆', '男', '中国'),                       -- director_id 35
('井上雄彦', '男', '日本'),                   -- director_id 36
('雷德利·斯科特', '男', '英国');              -- director_id 37 (已有)

-- 新增演员（ID 72-81）--
INSERT INTO actor_info (actor_name, type, country) VALUES
('沙梅克·摩尔', '男', '美国'),                -- actor_id 72
('克里斯·帕拉特', '男', '美国'),              -- actor_id 73
('基里安·墨菲', '男', '爱尔兰'),              -- actor_id 74 (已有)
('基努·里维斯', '男', '加拿大'),              -- actor_id 75 (已有)
('原菜乃华', '女', '日本'),                   -- actor_id 76
('保罗·路德', '男', '美国'),                  -- actor_id 77
('埃兹拉·米勒', '男', '美国'),                -- actor_id 78
('吴京', '男', '中国'),                       -- actor_id 79
('木村昂', '男', '日本'),                     -- actor_id 80
('华金·菲尼克斯', '男', '美国');               -- actor_id 81 (已有)

-- 导演-电影关系 --
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(22, 61),    -- 蜘蛛侠 - 乔伊姆·多斯·桑托斯(需补)
(25, 62),    -- 银河护卫队3 - 詹姆斯·古恩(需补)
(3, 63),     -- 奥本海默 - 诺兰 (已有)
(28, 64),    -- 疾速追杀4 - 查德·斯塔赫斯基(需补)
(34, 65),    -- 铃芽之旅 - 新海诚
(25, 66),    -- 蚁人3 - 佩顿·里德(需补)
(26, 67),    -- 闪电侠 - 安德斯·穆斯切蒂(需补)
(35, 68),    -- 流浪地球2 - 郭帆
(36, 69),    -- 灌篮高手 - 井上雄彦
(37, 70);    -- 拿破仑 - 斯科特 (已有)

-- 补充导演 --
INSERT INTO director_info (director_name, gender, country) VALUES
('乔伊姆·多斯·桑托斯', '男', '美国'),       -- director_id 38
('詹姆斯·古恩', '男', '美国'),               -- director_id 39
('查德·斯塔赫斯基', '男', '美国'),           -- director_id 40
('佩顿·里德', '男', '美国'),                 -- director_id 41
('安德斯·穆斯切蒂', '男', '阿根廷');          -- director_id 42

-- 更新导演-电影关系 --
UPDATE director_movie_relation SET director_id = 38 WHERE movie_id = 61;
UPDATE director_movie_relation SET director_id = 39 WHERE movie_id = 62;
UPDATE director_movie_relation SET director_id = 40 WHERE movie_id = 64;
UPDATE director_movie_relation SET director_id = 41 WHERE movie_id = 66;
UPDATE director_movie_relation SET director_id = 42 WHERE movie_id = 67;

-- 演员-电影关系 --
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 蜘蛛侠：纵横宇宙
(72, 61),             -- 摩尔
-- 银河护卫队3
(73, 62),             -- 帕拉特
-- 奥本海默
(74, 63),             -- 墨菲
-- 疾速追杀4
(75, 64),             -- 里维斯
-- 铃芽之旅
(76, 65),             -- 原菜乃华
-- 蚁人3
(77, 66),             -- 路德
-- 闪电侠
(78, 67),             -- 米勒
-- 流浪地球2
(79, 68),             -- 吴京
-- 灌篮高手
(80, 69),             -- 木村昂
-- 拿破仑
(81, 70);             -- 菲尼克斯

-- 角色信息 --
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 蜘蛛侠：纵横宇宙
(61, 72, '迈尔斯·莫拉莱斯/蜘蛛侠'),
-- 银河护卫队3
(62, 73, '星爵'),
-- 奥本海默
(63, 74, '罗伯特·奥本海默'),
-- 疾速追杀4
(64, 75, '约翰·威克'),
-- 铃芽之旅
(65, 76, '岩户铃芽'),
-- 蚁人3
(66, 77, '斯科特·朗/蚁人'),
-- 闪电侠
(67, 78, '巴里·艾伦/闪电侠'),
-- 流浪地球2
(68, 79, '刘培强'),
-- 灌篮高手
(69, 80, '宫城良田'),
-- 拿破仑
(70, 81, '拿破仑·波拿巴');

-- 添加新的出品公司（ID 13-15）
INSERT INTO production_company (company_name, city) VALUES
('东宝株式会社', '东京'),                  -- company_id 13 (忠犬八公)
('狮门影业', '圣莫尼卡'),                  -- company_id 14 (海豚湾)
('CJ娱乐', '首尔'),                       -- company_id 15 (心心历险记)
('日本电视放送网', '东京'),                -- company_id 16 (导盲犬小Q)
('北京缘起文化', '北京'),                  -- company_id 17 (二十二)
('CNEX', '北京'),                         -- company_id 18 (中国工厂)
('Uplink', '东京'),                       -- company_id 19 (坂本龙一)
('Atlas', '斯科普里');                    -- company_id 20 (蜜蜂之地)

-- 添加特殊演员（动物和旁白类型）(ID 82-92)
INSERT INTO actor_info (actor_name, type, country) VALUES
('八公(秋田犬)', '动物', '日本'),         -- actor_id 82
('海豚(太平洋)', '动物', '太平洋'),       -- actor_id 83
('心心(藏獒)', '动物', '中国'),           -- actor_id 84
('小Q(拉布拉多)', '动物', '日本'),        -- actor_id 85
('纪录片旁白', '旁白', '中国'),           -- actor_id 86 (二十二)
('工厂工人群像', '旁白', '中国'),         -- actor_id 87 (中国工厂)
('坂本龙一', '旁白', '日本'),             -- actor_id 88
('哈提兹', '旁白', '北马其顿'),           -- actor_id 89 (蜜蜂之地)
('养蜂人', '旁白', '北马其顿'),           -- actor_id 90
('蜜蜂群', '动物', '北马其顿'),           -- actor_id 91
('纪录片解说', '旁白', '国际');           -- actor_id 92 (海豚湾)

-- 添加这些特殊电影（ID 71-78）
INSERT INTO movie_info (movie_name, release_date, country, type, year, company_id) VALUES
('忠犬八公的故事', '2009-08-08', '日本', '剧情', 2009, 13),    -- movie_id 71
('海豚湾', '2009-07-31', '美国', '纪录片', 2009, 14),         -- movie_id 72
('心心历险记', '2010-06-30', '韩国', '冒险', 2010, 15),       -- movie_id 73
('导盲犬小Q', '2004-03-13', '日本', '剧情', 2004, 16),        -- movie_id 74
('二十二', '2017-08-14', '中国', '纪录片', 2017, 17),          -- movie_id 75
('中国工厂', '2019-11-22', '中国', '纪录片', 2019, 18),        -- movie_id 76
('坂本龙一：终曲', '2019-12-16', '日本', '纪录片', 2019, 19), -- movie_id 77
('蜜蜂之地', '2020-03-06', '北马其顿', '纪录片', 2020, 20);   -- movie_id 78

-- 添加导演（ID 43-50）
INSERT INTO director_info (director_name, gender, country) VALUES
('泷田洋二郎', '男', '日本'),              -- director_id 43 (忠犬八公)
('路易·西霍尤斯', '男', '美国'),           -- director_id 44 (海豚湾)
('朴英勋', '男', '韩国'),                  -- director_id 45 (心心历险记)
('崔洋一', '男', '日本'),                  -- director_id 46 (导盲犬小Q)
('郭柯', '男', '中国'),                    -- director_id 47 (二十二)
('萧潇', '女', '中国'),                    -- director_id 48 (中国工厂)
('史蒂芬·野村·斯奇博', '男', '美国'),      -- director_id 49 (坂本龙一)
('塔玛拉·科特夫斯卡', '女', '北马其顿');   -- director_id 50 (蜜蜂之地)

-- 导演-电影关系
INSERT INTO director_movie_relation (director_id, movie_id) VALUES
(43, 71),   -- 忠犬八公
(44, 72),   -- 海豚湾
(45, 73),   -- 心心历险记
(46, 74),   -- 导盲犬小Q
(47, 75),   -- 二十二
(48, 76),   -- 中国工厂
(49, 77),   -- 坂本龙一
(50, 78);   -- 蜜蜂之地

-- 演员-电影关系
INSERT INTO actor_movie_relation (actor_id, movie_id) VALUES
-- 忠犬八公
(82, 71),   -- 八公
-- 海豚湾
(83, 72), (92, 72),  -- 海豚, 解说
-- 心心历险记
(84, 73),   -- 心心
-- 导盲犬小Q
(85, 74),   -- 小Q
-- 二十二
(86, 75),   -- 旁白
-- 中国工厂
(87, 76),   -- 工人群像
-- 坂本龙一
(88, 77),   -- 本人
-- 蜜蜂之地
(89, 78), (90, 78), (91, 78);  -- 哈提兹, 养蜂人, 蜜蜂

-- 角色信息
INSERT INTO role_info (movie_id, actor_id, role_name) VALUES
-- 忠犬八公
(71, 82, '八公'),
-- 海豚湾
(72, 83, '海豚'), (72, 92, '纪录片解说'),
-- 心心历险记
(73, 84, '心心'),
-- 导盲犬小Q
(74, 85, '小Q'),
-- 二十二
(75, 86, '历史见证者旁白'),
-- 中国工厂
(76, 87, '工人群体叙述'),
-- 坂本龙一
(77, 88, '自我讲述'),
-- 蜜蜂之地
(78, 89, '哈提兹'), (78, 90, '养蜂人'), (78, 91, '蜜蜂群');
