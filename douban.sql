SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


DROP TABLE IF EXISTS books;
CREATE TABLE books (
  id int(10) UNSIGNED NOT NULL,
  slug varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  sub_name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  alt_name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  cover varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  summary text COLLATE utf8mb4_unicode_ci,
  authors varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  author_intro text COLLATE utf8mb4_unicode_ci,
  translators varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  series varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  publisher varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  publish_date varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  pages varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  price varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  binding varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  isbn varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  tags varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  douban_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  douban_score decimal(3,1) UNSIGNED NOT NULL DEFAULT '0.0',
  douban_votes int(10) UNSIGNED NOT NULL DEFAULT '0',
  created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  updated_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  id int(10) UNSIGNED NOT NULL,
  douban_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  douban_comment_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  douban_user_nickname varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  douban_user_avatar varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  douban_user_url varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  content text COLLATE utf8mb4_unicode_ci NOT NULL,
  votes int(10) UNSIGNED NOT NULL DEFAULT '0',
  created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  updated_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
  id int(10) UNSIGNED NOT NULL,
  type varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  slug varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  alias varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  cover varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  year smallint(5) UNSIGNED NOT NULL DEFAULT '0',
  regions varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  genres varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  languages varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  release_date date DEFAULT NULL,
  official_site varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  directors varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  actors text COLLATE utf8mb4_unicode_ci,
  storyline text COLLATE utf8mb4_unicode_ci,
  mins smallint(5) UNSIGNED NOT NULL DEFAULT '0',
  recommend_tip varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  tags varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  avg_score decimal(3,1) UNSIGNED NOT NULL DEFAULT '0.0',
  imdb_id varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  imdb_score decimal(3,1) UNSIGNED NOT NULL DEFAULT '0.0',
  imdb_votes int(10) UNSIGNED NOT NULL DEFAULT '0',
  douban_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  douban_score decimal(3,1) UNSIGNED NOT NULL DEFAULT '0.0',
  douban_votes int(10) UNSIGNED NOT NULL DEFAULT '0',
  created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  updated_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
  id int(10) UNSIGNED NOT NULL,
  douban_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  type enum('movie','book') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'movie'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE books
  ADD PRIMARY KEY (id),
  ADD KEY books_slug_index (slug),
  ADD KEY books_name_index (name),
  ADD KEY books_douban_id_index (douban_id);

ALTER TABLE comments
  ADD PRIMARY KEY (id),
  ADD KEY comments_douban_id_index (douban_id),
  ADD KEY comments_douban_comment_id_index (douban_comment_id);

ALTER TABLE movies
  ADD PRIMARY KEY (id),
  ADD KEY movies_slug_index (slug),
  ADD KEY movies_name_index (name),
  ADD KEY movies_imdb_id_index (imdb_id),
  ADD KEY movies_douban_id_index (douban_id);

ALTER TABLE subjects
  ADD PRIMARY KEY (id),
  ADD UNIQUE KEY subjects_douban_id_unique (douban_id);


ALTER TABLE books
  MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
ALTER TABLE comments
  MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
ALTER TABLE movies
  MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
ALTER TABLE subjects
  MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
