INSERT INTO core_user (`username`, `password`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`,`is_superuser`, `date_joined`)
VALUES
('johndoe', 'pbkdf2_sha256$150000$7aNHwmRzYSf7$fWc+8zvUb9RkKjz+WJf1+Y8b0cyvytOpC0qJ3yHsdbI=', 'John', 'Doe', 'johndoe@example.com', 1, 1, 0, '2022-01-01 00:00:00'),
('janedoe', 'pbkdf2_sha256$150000$NKhRDhOtGKjN$c8hbGTF9Xx43RIVZbNz+SS8M/BrD7KtKKk3tq3vw1cg=', 'Jane', 'Doe', 'janedoe@example.com', 0, 0, 0, '2022-01-01 00:00:00'),
('bobsmith', 'pbkdf2_sha256$150000$U6kceU6c0r6M$uD5LnbZzVcLM12avfCB05dIUTj6Ua7vkUaH6psv2FqQ=', 'Bob', 'Smith', 'bobsmith@example.com', 0, 1, 0, '2022-01-01 00:00:00'),
('amandajohnson', 'pbkdf2_sha256$150000$3Qy/bLD0nBrv$1Czg4CF4rjU+4Lk5jBr0W8l4J4Y/R5nb5KjD5UW0Ehc=', 'Amanda', 'Johnson', 'amandajohnson@example.com', 1, 1, 0, '2022-01-01 00:00:00'),
('markwilson', 'pbkdf2_sha256$150000$y5G5J5COE+YY$SvPn/26Jwz70P8boNH75YUIY+Jjg9hyxjyzas3IqNmlU=', 'Mark', 'Wilson', 'markwilson@example.com', 0, 1, 0, '2022-01-01 00:00:00');

INSERT INTO core_trainee (birthdate, height, weight, daily_calories_needs, daily_calories_intake, daily_water_intake, daily_water_needs, carbs_ratio, fats_ratio, protein_ratio, was_active_today, daily_streak, activity_level, goal, user_id)
VALUES
  ('1990-12-15', 168.5, 65.0, 1800.0, 1600.0, 2500, 2000, 0.4, 0.4, 0.2, 1, 2, 'M', 'L', 1),
  ('1998-08-01', 186.0, 80.0, 2200.0, 2100.0, 3000, 3500, 0.3, 0.5, 0.2, 0, 1, 'L', 'L', 2),
  ('1993-03-22', 174.0, 55.0, 1600.0, 1500.0, 2500, 2000, 0.5, 0.3, 0.2, 1, 5, 'M', 'G', 3),
  ('2000-11-07', 186.0, 75.0, 2000.0, 1900.0, 2000, 2500, 0.4, 0.4, 0.2, 0, 1, 'H', 'K', 4),
  ('1995-05-10', 172.0, 70.0, 2000.0, 1800.0, 2000, 2500, 0.5, 0.3, 0.2, 1, 3, 'H', 'G', 5);
  
INSERT INTO `diet_food` (`id`, `name`, `category`, `calories`, `carbs`, `fats`, `protein`) VALUES
(1, 'Grilled chicken breast', 'F', 180.0, 0.0, 4.0, 36.0),
(2, 'Beef steak', 'F', 250.0, 0.0, 15.0, 28.0),
(3, 'Salmon fillet', 'F', 220.0, 0.0, 13.0, 23.0),
(4, 'Brown rice', 'F', 218.0, 46.0, 2.0, 5.0),
(5, 'Quinoa', 'F', 120.0, 21.0, 2.0, 4.0),
(6, 'Lentils', 'F', 230.0, 40.0, 1.5, 18.0),
(7, 'Spinach', 'F', 23.0, 3.6, 0.4, 2.9),
(8, 'Broccoli', 'F', 55.0, 10.0, 1.0, 4.0),
(9, 'Carrots', 'F', 41.0, 10.0, 0.2, 1.0),
(10, 'Apples', 'F', 95.0, 25.0, 0.3, 0.5),
(11, 'Bananas', 'F', 105.0, 27.0, 0.4, 1.3),
(12, 'Almonds', 'F', 575.0, 22.0, 49.0, 21.0),
(13, 'Peanut butter', 'F', 190.0, 6.0, 16.0, 7.0),
(14, 'Greek yogurt', 'F', 100.0, 7.0, 0.4, 18.0),
(15, 'Whey protein powder', 'F', 120.0, 2.0, 1.0, 25.0),
(16, 'Green tea', 'B', 0.0, 0.0, 0.0, 0.0),
(17, 'Black coffee', 'B', 0.0, 0.0, 0.0, 0.0),
(18, 'Orange juice', 'B', 112.0, 26.0, 0.5, 2.0),
(19, 'Water', 'B', 0.0, 0.0, 0.0, 0.0),
(20, 'Salt', 'S', 0.0, 0.0, 0.0, 0.0);

INSERT INTO diet_custom_food (food_ptr_id, trainee_id) VALUES
    (14, 4),
    (15, 4),
    (16, 4),
    (17, 4),
    (18, 5),
    (19, 5),
    (20, 5);

INSERT INTO `diet_recipe` (`name`, `instructions`, `trainee_id`) VALUES
  ('Chicken Stir Fry', 'Stir fry chicken with vegetables and serve over rice.', 1),
  ('Veggie Omelette', 'Whisk eggs, add vegetables, and cook until golden brown.', 2),
  ('Beef Tacos', 'Season and cook beef, serve in taco shells with toppings.', 3),
  ('Avocado Toast', 'Toast bread, spread avocado, and add toppings.', 4),
  ('Pesto Pasta', 'Cook pasta, mix pesto sauce and serve.', 5);
  
INSERT INTO `diet_meal` (`name`, `time_eaten`, `trainee_id`) VALUES
  ('Breakfast', '2022-01-01 08:00:00', 1),
  ('Lunch', '2022-01-01 12:00:00', 1),
  ('Dinner', '2022-01-01 19:00:00', 1),
  ('Breakfast', '2022-01-02 08:00:00', 2),
  ('Lunch', '2022-01-02 12:00:00', 2);
  
INSERT INTO `diet_food_instance` (`quantity`, `food_id`, `recipe_id`)
VALUES
    (2.5, 1, 1),
    (3, 2, 2),
    (1, 3, 3),
    (4, 4, 4),
    (1.5, 5, 5),
    (2, 6, 5),
    (1.5, 7, 4),
    (3, 8, 3),
    (2, 9, 2),
    (4, 10, 1),
    (1, 11, 2),
    (2.5, 12, 3),
    (3, 13, 4),
    (1, 14, 5),
    (4, 15, 2),
    (1.5, 16, 3),
    (2, 17, 4),
    (1.5, 18, 5),
    (3, 19, 1),
    (2, 20, 2);
    