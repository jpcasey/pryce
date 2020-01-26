--TODO
DROP TABLE IF EXISTS chain CASCADE;
CREATE TABLE chain (
  chain_id int GENERATED BY DEFAULT AS IDENTITY,
  PRIMARY KEY(chain_id)
);

--TODO
DROP TABLE IF EXISTS access CASCADE;
CREATE TABLE access (
  access_id int GENERATED BY DEFAULT AS IDENTITY,
  PRIMARY KEY(access_id)
);

DROP TABLE IF EXISTS list CASCADE;
CREATE TABLE list (
  list_id int GENERATED BY DEFAULT AS IDENTITY,
  owner int,
  --TODO
  access_id int,
  PRIMARY KEY (list_id)
);

DROP TABLE IF EXISTS image CASCADE;
CREATE TABLE image (
  image_id int GENERATED BY DEFAULT AS IDENTITY,
  fspath varchar,
  imgtype varchar,
  width int,
  height int,
  PRIMARY KEY (image_id)
);

DROP TABLE IF EXISTS item CASCADE;
CREATE TABLE item (
  item_id int GENERATED BY DEFAULT AS IDENTITY,
  code varchar NOT NULL,
  name varchar NOT NULL,
  brand varchar,
  weight numeric NOT NULL,
  --TODO: CONSTRAINT on values for unit
  weight_unit varchar DEFAULT 'oz',
  image_id int,
  description text NOT NULL,
  PRIMARY KEY (item_id)
);

DROP TABLE IF EXISTS list_item CASCADE;
CREATE TABLE list_item (
  item_id bigint,
  list_id bigint REFERENCES list (list_id),
  quantity int DEFAULT 1,
  PRIMARY KEY (item_id, list_id)
);

DROP TABLE IF EXISTS usr CASCADE;
CREATE TABLE usr (
  usr_id int GENERATED BY DEFAULT AS IDENTITY,
  usrname varchar,
  password varchar,
  home int,
  karma int,
  avatar int,
  --TODO: an account table with things like start date and in/active bool
  --account_id int,
  PRIMARY KEY (usr_id)
);

DROP TABLE IF EXISTS location CASCADE;
CREATE TABLE location (
  location_id int GENERATED BY DEFAULT AS IDENTITY,
  lat real,
  long real,
  PRIMARY KEY (location_id)
);

DROP TABLE IF EXISTS comment CASCADE;
CREATE TABLE comment (
  object_id int,
  usr_id int NOT NULL,
  rating numeric,
  content text,
  type int, 
  PRIMARY KEY (object_id, type)
);

DROP TABLE IF EXISTS price CASCADE;
CREATE TABLE price (
  price_id int GENERATED BY DEFAULT AS IDENTITY,
  currency varchar(3),
  item_id int,
  usr_id int,
  price  money,
  reported timestamptz,
  store_id int,
  PRIMARY KEY (price_id)
);


DROP TABLE IF EXISTS store CASCADE;
CREATE TABLE store (
  store_id int GENERATED BY DEFAULT AS IDENTITY,
  location_id int,
  --TODO
  chain_id int,
  name varchar,
  image_id int,
  PRIMARY KEY (store_id)
);


DROP TABLE IF EXISTS badge_usr CASCADE;
CREATE TABLE badge_usr (
  badge_id int GENERATED BY DEFAULT AS IDENTITY,
  usr_id int,
  PRIMARY KEY (badge_id, usr_id)
);

DROP TABLE IF EXISTS badge CASCADE;
CREATE TABLE badge (
  badge_id int GENERATED BY DEFAULT AS IDENTITY,
  name varchar,
  image_id bigint,
  PRIMARY KEY (badge_id)
);

/*
 * CONSTRAINTS
 */
--list to usr
ALTER TABLE list ADD CONSTRAINT fk_owner FOREIGN KEY (owner) REFERENCES usr(usr_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE list ADD CONSTRAINT fk_access_id FOREIGN KEY (access_id) REFERENCES access(access_id) ON UPDATE CASCADE ON DELETE RESTRICT;

--item to image and item unique constraint
ALTER TABLE item ADD CONSTRAINT fk_image_id FOREIGN KEY (image_id) REFERENCES image(image_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE item ADD CONSTRAINT uq_code_weight UNIQUE (code);

--list_item to item
ALTER TABLE list_item ADD CONSTRAINT fk_item_id FOREIGN KEY (item_id) REFERENCES item(item_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE list_item ADD CONSTRAINT fk_list_id FOREIGN KEY (list_id) REFERENCES list(list_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- image unique path
ALTER TABLE image ADD CONSTRAINT uq_fspath UNIQUE (fspath);

-- usr to image and usr to location
ALTER TABLE usr ADD CONSTRAINT uq_usrname UNIQUE (usrname);
ALTER TABLE usr ADD CONSTRAINT fk_image_id FOREIGN KEY (avatar) REFERENCES image(image_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE usr ADD CONSTRAINT fk_location_id FOREIGN KEY (home) REFERENCES location(location_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- comment review and content both NOT NULL
ALTER TABLE comment ADD CONSTRAINT ck_content_rating CHECK (content is NOT NULL OR rating is NOT NULL);
ALTER TABLE comment ADD CONSTRAINT fk_usr_id FOREIGN KEY (usr_id) REFERENCES usr(usr_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- price
ALTER TABLE price ADD CONSTRAINT fk_usr_id FOREIGN KEY (usr_id) REFERENCES usr(usr_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE price ADD CONSTRAINT fk_store_id FOREIGN KEY (store_id) REFERENCES store(store_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE price ADD CONSTRAINT fk_item_id FOREIGN KEY (item_id) REFERENCES item(item_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- store
ALTER TABLE store ADD CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES location(location_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE store ADD CONSTRAINT fk_image_id FOREIGN KEY (image_id) REFERENCES image(image_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE store ADD CONSTRAINT fk_chain_id FOREIGN KEY (chain_id) REFERENCES chain(chain_id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- badge_usr
ALTER TABLE badge_usr ADD CONSTRAINT fk_usr_id FOREIGN KEY (usr_id) REFERENCES usr(usr_id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE badge_usr ADD CONSTRAINT fk_badge_id FOREIGN KEY (badge_id) REFERENCES badge(badge_id) ON UPDATE CASCADE ON DELETE RESTRICT;

