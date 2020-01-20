CREATE TABLE "List_Product" (
  "ProductId" bigint,
  "ListId" bigint,
  "Quantity" int
);

CREATE INDEX "PK, FK" ON  "List_Product" ("ProductId", "ListId");

CREATE TABLE "Badge_User" (
  "BadgeId" bigint,
  "UserId" bigint
);

CREATE INDEX "PK, FK" ON  "Badge_User" ("BadgeId", "UserId");

CREATE TABLE "Comment" (
  "CommentId" bigint,
  "ObjectId" bigint,
  "UserId" bigint,
  "Rating" real,
  "Content" text,
  PRIMARY KEY ("CommentId")
);

CREATE INDEX "FK" ON  "Comment" ("ObjectId", "UserId");

CREATE TABLE "Product" (
  "ProductId" bigint,
  "Code" varchar,
  "Name" varchar,
  "Brand" varchar,
  "Weight" real,
  "WeightUnit" varchar,
  "ImageId" bigint,
  "Description" text,
  PRIMARY KEY ("ProductId")
);

CREATE INDEX "FK" ON  "Product" ("ImageId");

CREATE TABLE "User" (
  "UserId" bigint,
  "Username" varchar,
  "Password" varchar,
  "Home" bigint,
  "Karma" int,
  "BadgeId" bigint,
  "Avatar" bigint,
  PRIMARY KEY ("UserId")
);

CREATE INDEX "FK" ON  "User" ("Home", "BadgeId", "Avatar");

CREATE TABLE "Location" (
  "LocationId" bigint,
  "Lat" real,
  "Long" real,
  PRIMARY KEY ("LocationId")
);

CREATE TABLE "Price" (
  "PriceId" bigint,
  "Currency" varchar,
  "ProductId" int,
  "UserId" bigint,
  " Price"  real,
  "Reported" timestamptz,
  "StoreId" bigint,
  PRIMARY KEY ("PriceId")
);

CREATE INDEX "FK" ON  "Price" ("ProductId", "UserId", "StoreId");

CREATE TABLE "Image" (
  "ImageId" bigint,
  "Path" varchar,
  "Type" varchar,
  "Width" int,
  "Height" int,
  PRIMARY KEY ("ImageId")
);

CREATE TABLE "Store" (
  "StoreId" bigint,
  "LocationId" bigint,
  "ChainId" bigint,
  "Name" varchar,
  "ImageId" bigint,
  PRIMARY KEY ("StoreId")
);

CREATE INDEX "FK" ON  "Store" ("LocationId", "ChainId", "ImageId");

CREATE TABLE "List" (
  "ListId" bigint,
  "OwnerId" bigint,
  "AccessId" bigint,
  PRIMARY KEY ("ListId")
);

CREATE INDEX "FK" ON  "List" ("OwnerId", "AccessId");

CREATE TABLE "Badge" (
  "BadgeId" bigint,
  "Name" varchar,
  "ImageId" bigint,
  PRIMARY KEY ("BadgeId")
);

CREATE INDEX "FK" ON  "Badge" ("ImageId");


