DROP TABLE IF EXISTS tags_post;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS imp_user;




CREATE TABLE imp_user (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES imp_user (id)
);

CREATE TABLE tag (
       id SERIAL PRIMARY KEY,
       name TEXT UNIQUE NOT NULL
              ); 
       
CREATE TABLE tags_post (
       notes INTEGER,
       tag INTEGER,
       FOREIGN KEY (notes) references post(id) ON DELETE CASCADE,
       FOREIGN KEY (tag) references tag(id) ON DELETE CASCADE
);

       

