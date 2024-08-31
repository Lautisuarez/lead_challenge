CREATE TABLE Career (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Subject (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    career_id INT,
    FOREIGN KEY (career_id) REFERENCES Career(ID)
);

CREATE TABLE Lead (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE Course (
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    inscription_year VARCHAR(4) NOT NULL,
    lead_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES Lead(ID),
    FOREIGN KEY (subject_id) REFERENCES Subject(ID)
);