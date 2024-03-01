CREATE TABLE engineer (
  id SERIAL PRIMARY KEY,
  username VARCHAR(12) NOT NULL,
  password VARCHAR(255) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  name VARCHAR(100) NOT NULL,
  patronymic VARCHAR(100) NOT NULL,
  working_position VARCHAR(70) NOT NULL,
  city VARCHAR(30) NOT NULL,
  phone_number VARCHAR(11) NOT NULL,
  email VARCHAR(50),
  created_on DATE NOT NULL
);

INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('admin', 'admin', 'Фомин', 'Алексей', 'Геннадьевич', 'Разработчик', 'Москва', '89995534590', 'admin_email', CURRENT_DATE);
INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('инженер1', 'pass1', 'Иванов', 'Алексей', 'Петрович', 'Инженер-программист', 'Москва', '89938834593', 'ivanov_email', CURRENT_DATE);
INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('инженер2', 'pass2', 'Смирнова', 'Екатерина', 'Александровна', 'Разработчик', 'Москва', '8997234291', 'smirnova_email', CURRENT_DATE);
INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('инженер3', 'pass3', 'Петров', 'Дмитрий', 'Игоревич', 'Инженер-программист', 'Москва', '8931847398', 'petrov_email', CURRENT_DATE);
INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('инженер4', 'pass4', 'Сидорова', 'Ольга', 'Владимировна', 'Разработчик', 'Москва', '89931209491', 'sidorova_email', CURRENT_DATE);
INSERT INTO engineer (username, password, last_name, name, patronymic, working_position, city, phone_number, email, created_on) VALUES ('инженер5', 'pass5', 'Кузнецов', 'Алексей', 'Николаевич', 'Инженер-технолог', 'Москва', '89931234598', 'kuznecov_email', CURRENT_DATE);

CREATE TABLE direction (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

INSERT INTO direction (name) VALUES ('SDH');
INSERT INTO direction (name) VALUES ('СПД');
INSERT INTO direction (name) VALUES ('Сервера');
INSERT INTO direction (name) VALUES ('PDH');
INSERT INTO direction (name) VALUES ('WDM');
INSERT INTO direction (name) VALUES ('ОбТС');

CREATE TABLE engineer_direction (
  engineer_id INTEGER,
  direction_id INTEGER,
  PRIMARY KEY (engineer_id, direction_id),
  FOREIGN KEY (engineer_id) REFERENCES engineer (id),
  FOREIGN KEY (direction_id) REFERENCES direction (id)
);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (2, 1);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (2, 4);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (2, 5);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (3, 2);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (3, 3);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (4, 6);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (4, 4);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (5, 3);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (5, 5);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (6, 6);
INSERT INTO engineer_direction (engineer_id, direction_id) VALUES (6, 2);

CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

INSERT INTO status (name) VALUES ('Принят');
INSERT INTO status (name) VALUES ('В работе');
INSERT INTO status (name) VALUES ('Завершен');

CREATE TABLE task (
  id SERIAL PRIMARY KEY,
  description VARCHAR(255) NOT NULL,
  direction_id INTEGER,
  status_id INTEGER,
  engineer_id INTEGER,
  create_date DATE,
  FOREIGN KEY (direction_id) REFERENCES direction (id),
  FOREIGN KEY (status_id) REFERENCES status (id),
  FOREIGN KEY (engineer_id) REFERENCES engineer (id)
);

INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 1, 1, 2, '2024-02-02');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 1, 1, 2, '2024-02-02');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 1, 1, 2, '2024-02-02');

INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 3, '2024-01-30');

INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 6, 1, 4, '2024-02-02');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 6, 1, 4, '2024-02-02');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 6, 1, 4, '2024-02-02');

INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 3, 1, 5, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 3, 1, 5, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 3, 1, 5, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 3, 1, 5, '2024-01-30');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 3, 1, 5, '2024-01-30');

INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 6, '2024-01-31');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 6, '2024-01-31');
INSERT INTO task (description, direction_id, status_id, engineer_id, create_date) VALUES ('Описание задачи', 2, 1, 6, '2024-01-31');

CREATE TABLE vacation (
  id SERIAL PRIMARY KEY,
  engineer_id INTEGER,
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (engineer_id) REFERENCES engineer (id)
);

INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (1, '2024-06-15', '2024-06-29');
INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (2, '2024-02-05', '2024-02-15');
INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (3, '2024-02-07', '2024-02-09');
INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (4, '2024-06-05', '2024-06-12');
INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (5, '2024-02-12', '2024-02-15');
INSERT INTO vacation (engineer_id, start_date, end_date) VALUES (6, '2024-02-07', '2024-02-09');
