-- Adminer 4.8.1 PostgreSQL 15.3 (Debian 15.3-1.pgdg110+1) dump
-- Create extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS "passwords";
CREATE TABLE "public"."passwords" (
    "password_id" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "user_id" uuid NOT NULL,
    "password" character varying(255) NOT NULL,
    CONSTRAINT "passwords_pkey" PRIMARY KEY ("password_id")
) WITH (oids = false);

DROP TABLE IF EXISTS "roles";
CREATE TABLE "public"."roles" (
    "role_id" smallint DEFAULT '1' NOT NULL,
    "role_name" character varying NOT NULL,
    CONSTRAINT "roles_role_id" PRIMARY KEY ("role_id")
) WITH (oids = false);

DROP TABLE IF EXISTS "users";
CREATE TABLE "public"."users" (
    "user_id" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "user_first_name" character varying NOT NULL,
    "user_last_name" character varying NOT NULL,
    "user_email" character varying NOT NULL,
    "user_role" smallint DEFAULT '1' NOT NULL,
    CONSTRAINT "user_pkey" PRIMARY KEY ("user_id"),
    CONSTRAINT "users_user_email" UNIQUE ("user_email")
) WITH (oids = false);

DROP TABLE IF EXISTS "carte";
CREATE TABLE "public"."carte" (
    "carte_id" uuid DEFAULT uuid_generate_v4() NOT NULL,
    "carte_number" character varying NOT NULL,
    "carte_validity_year" character varying NOT NULL,
    "carte_study_year" character varying NOT NULL,
    "carte_user_id" uuid NOT NULL,
    CONSTRAINT "carte_pkey" PRIMARY KEY ("carte_id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."passwords"
    ADD CONSTRAINT "passwords_user_id_fkey"
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_user_role_fkey"
    FOREIGN KEY (user_role) REFERENCES roles(role_id)
    ON UPDATE CASCADE ON DELETE SET DEFAULT NOT DEFERRABLE;

ALTER TABLE ONLY "public"."carte"
    ADD CONSTRAINT "users_carte_user_fkey"
    FOREIGN KEY (carte_user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE SET DEFAULT NOT DEFERRABLE;

-- 2023-06-08 16:07:50.896571+00

-- Generate default Roles
INSERT INTO "roles" (role_id, role_name)
VALUES
(1, 'admin'),
(2, 'student');


-- Generate default users
INSERT INTO "users" (user_id, user_first_name, user_last_name, user_email, user_role)
VALUES
    ('00000000-0000-0000-0000-000000000001',
     'default', 'admin', 'default@admin.com', 1);

-- Generate passwords for users
INSERT INTO "passwords" (password_id, user_id, password)
VALUES
    ('00000000-0000-0000-0000-000000000101',
     '00000000-0000-0000-0000-000000000001',
     '$argon2id$v=19$m=65536,t=3,p=4$L1SGzOM6joPhlb8Out4dAg$exuTB0l39jlzy0m/ItJHBPI16vO6rVQCgI9ousD6lA8');
