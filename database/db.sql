CREATE SEQUENCE roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE roles_id_seq OWNED BY roles.id;

CREATE TABLE roles (
    id bigint NOT NULL DEFAULT nextval('roles_id_seq'),
    name character varying(20) NOT NULL,
    PRIMARY KEY (id)
);


CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_id_seq OWNED BY users.id;

CREATE TABLE users (
    id bigint NOT NULL DEFAULT nextval('users_id_seq'),
    PRIMARY KEY (id),
    first_name character varying(100) NOT NULL,
    last_name character varying(100),
    password character varying(100),
    phone_number character(12) NOT NULL,
    email character(100),
    is_active boolean DEFAULT true,
    role_id bigint NOT NULL,
    CONSTRAINT fk_user_role
      FOREIGN KEY(role_id)
	  REFERENCES roles(id)
);

CREATE SEQUENCE country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE country_id_seq OWNED BY countries.id;

CREATE TABLE countries(
    id bigint NOT NULL DEFAULT nextval('country_id_seq'),
    PRIMARY KEY (id),
    name character varying(40) NOT NULL
);

CREATE SEQUENCE city_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE city_id_seq OWNED BY cities.id;

CREATE TABLE cities(
    id bigint NOT NULL DEFAULT nextval('city_id_seq'),
    PRIMARY KEY (id),
    name character varying(50) NOT NULL,
    country_id bigint NOT NULL,
    CONSTRAINT fk_country_cities
        FOREIGN KEY(country_id)
	    REFERENCES countries(id)
	    ON DELETE CASCADE
);

CREATE SEQUENCE place_address_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE place_address_id_seq OWNED BY place_addresses.id;

CREATE TABLE place_addresses(
    id bigint NOT NULL DEFAULT nextval('place_address_id_seq'),
    PRIMARY KEY (id),
    street character varying(150) NOT NULL,
    building character varying(30) NOT NULL,
    latitude decimal,
    longitude decimal,
    country_id bigint NOT NULL,
    CONSTRAINT fk_place_address_country
        FOREIGN KEY(country_id)
	    REFERENCES countries(id),
    city_id bigint NOT NULL,
    CONSTRAINT fk_place_address_city
        FOREIGN KEY(city_id)
	    REFERENCES cities(id)
);

CREATE SEQUENCE place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE place_id_seq OWNED BY places.id;

CREATE TABLE places(
    id bigint NOT NULL DEFAULT nextval('place_id_seq'),
    PRIMARY KEY (id),
    title character varying(150) NOT NULL,
    place_description character varying(150),
    place_url character varying(150),
    avatar character varying(200),
    email character varying(100),
    phone character varying(15),
    type_place character varying(50),
    owner_id bigint NOT NULL,
    CONSTRAINT fk_place_owner
        FOREIGN KEY(owner_id)
	    REFERENCES users(id)
);

CREATE SEQUENCE place_branch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE place_branch_id_seq OWNED BY place_branches.id;

CREATE TABLE place_branches(
    id bigint NOT NULL DEFAULT nextval('place_branch_id_seq'),
    PRIMARY KEY (id),
    place_id bigint NOT NULL,
    CONSTRAINT fk_place_branches_place
        FOREIGN KEY(place_id)
	    REFERENCES places(id),
    place_address_id bigint NOT NULL,
    CONSTRAINT fk_place_branches_address
        FOREIGN KEY(place_address_id)
	    REFERENCES place_addresses(id),
    created_at timestamp NOT NULL DEFAULT NOW()
);

CREATE SEQUENCE users_to_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_to_place_id_seq OWNED BY users_to_places.id;

CREATE TABLE users_to_places(
    id bigint NOT NULL DEFAULT nextval('users_to_place_id_seq'),
    PRIMARY KEY (id),
    is_favourite boolean DEFAULT true,
    user_id bigint NOT NULL,
    CONSTRAINT fk_user_to_place
        FOREIGN KEY(user_id)
	    REFERENCES users(id),
    place_branch_id bigint NOT NULL,
    CONSTRAINT fk_place_to_user
        FOREIGN KEY(place_branch_id)
	    REFERENCES place_branches(id),
    UNIQUE (user_id, place_branch_id)
);

CREATE SEQUENCE table_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE table_id_seq OWNED BY tables.id;

CREATE TABLE tables(
    id bigint NOT NULL DEFAULT nextval('table_id_seq'),
    PRIMARY KEY (id),
    table_number INT NOT NULL,
    max_people INT NOT NULL,
    is_electricity boolean DEFAULT false,
    floor INT NOT NULL,
    is_available boolean DEFAULT true,
    place_branch_id bigint NOT NULL,
    CONSTRAINT fk_table_place
        FOREIGN KEY(place_branch_id)
	    REFERENCES place_branches(id),
    UNIQUE (table_number, place_branch_id)
);

CREATE SEQUENCE reservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE reservation_id_seq OWNED BY reservations.id;

CREATE TABLE reservations(
    id bigint NOT NULL DEFAULT nextval('reservation_id_seq'),
    PRIMARY KEY (id),
    amount guests INT,
    date_reservation date NOT NULL,
    time_start time without time zone NOT NULL,
    time_end time without time zone NOT NULL,
    note character varying(250),
    celebration character varying(100),
    user_id bigint NOT NULL,
    CONSTRAINT fk_reservation_user
        FOREIGN KEY(user_id)
	    REFERENCES users(id),
    table_id bigint NOT NULL,
    CONSTRAINT fk_reservation_table
        FOREIGN KEY(table_id)
	    REFERENCES tables(id)
);

CREATE SEQUENCE media_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE media_file_id_seq OWNED BY media_files.id;

CREATE TABLE media_files(
    id bigint NOT NULL DEFAULT nextval('media_file_id_seq'),
    PRIMARY KEY (id),
    source_id character varying(100) NOT NULL,
    source_fields json,
    source_url character varying(200),
    uploaded boolean DEFAULT false,
    created_at timestamp NOT NULL DEFAULT NOW(),
    filename varchar NOT NULL,
    user_id bigint NOT NULL,
    CONSTRAINT fk_media_file_user
        FOREIGN KEY(user_id)
	    REFERENCES users(id)
);

CREATE SEQUENCE place_to_media_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE place_to_media_file_id_seq OWNED BY place_to_media_file.id;

CREATE TABLE place_to_media_file(
    id bigint NOT NULL DEFAULT nextval('place_to_media_file_id_seq'),
    PRIMARY KEY (id),
    place_branch_id bigint NOT NULL,
    CONSTRAINT fk_place_to_media_file
        FOREIGN KEY(place_branch_id)
	    REFERENCES place_branches(id),
    media_file_id bigint NOT NULL,
    CONSTRAINT fk_media_file_to_place
        FOREIGN KEY(media_file_id)
	    REFERENCES media_files(id)
);
