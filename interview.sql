-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2025 at 09:02 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `interview`
--

-- --------------------------------------------------------

--
-- Table structure for table `candidates`
--

CREATE TABLE `candidates` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `photoUrl` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidates`
--

INSERT INTO `candidates` (`id`, `name`, `email`, `photoUrl`) VALUES
(1, 'Bambang', 'bambang@gmail.com', ''),
(5, 'Melania Intan', 'melaniaintan@gmail.com', 'https://i.pinimg.com/736x/10/be/fa/10befad13247f1ee2a82ac7a81496575.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `final_result`
--

CREATE TABLE `final_result` (
  `id` int(11) NOT NULL,
  `interview_id` int(11) NOT NULL,
  `final_result` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `input`
--

CREATE TABLE `input` (
  `id` int(11) NOT NULL,
  `interview_id` int(11) NOT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `result_cd` varchar(200) NOT NULL,
  `result_stt` varchar(3000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `input`
--

INSERT INTO `input` (`id`, `interview_id`, `file_name`, `result_cd`, `result_stt`) VALUES
(6, 26, 'tmpi_9lbvk1.webm', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Can you share any specific challenges you faced while working on certification and how you overcame them?\", \"Answer\": \" Can you share any specific challenges you faced while working on certification and how you overcome them? Ah, okay, actually, for the challenges, there are some challenges when I took the certification, especially for the project I mentioned that I already working with it. the first one is actually to meet the specific accuracy or fallition loss for the evaluation matrix and yeah actually that just need to take some trial and error with different architecture for example like we can try to add more layer, more neurons, changes the neurons or even I also apply the dropout layer so yeah it really helps with the the validation loss to to become more lower right and yeah I think that\'s that\'s one of the biggest challenges that I have while working on these certifications\"}'),
(7, 26, 'tmpgul2gter.webm', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Can you describe your experience with transfer learning in TensorFlow? How did it benefit your projects?\", \"Answer\": \" can you describe your experience with transfer learning and time short flow? how do you benefit from projects? about transfer learning is actually we use existing train model from time short flow for example like VGC16, VGC19 especially for some cases that we need to use deep learning using Keras applications for example like image classification we can use transfer learning models which is that\'s already trained model with exceptionally high accuracy high performance yeah even though it\'s trained with different data sets but it really helps to improve our model performance, model accuracy, model loss and for example like mobile net, VGG19, VGG16, efficient net, it will help to improve our models comparing to the one if you use a traditional CNN model yeah CNN model with the convolutional 2d yeah max pooling and yeah it it\'s it\'s quite good actually to use transfer learning it really helps with our model performance to improve our model performance.\"}'),
(8, 26, 'tmpbksbhk33.webm', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Describe a complex TensorFlow model you have built and the steps you took to ensure its accuracy and efficiency.\", \"Answer\": \" wait what is this? describe a complex TensorFlow model you have built and the steps you took to ensure its accuracy and efficiency hmmm... complex TensorFlow model you have built and steps you took to ensure its accuracy okay I will take one of my previous project that I use yeah I also use Keras or TensorFlow model it\'s it is about a cellular disease prediction yeah yeah this is also I use the research project for my undergraduate thesis yeah for my script C and I use this model it\'s quite challenging even though it\'s achieved high accuracy with some dense layer yeah with some drawout layer and trial and error also with the callback function with the neurons but the problem is the dataset is not balanced so it has the imbalanced class datasets and the approach that I use is to just to use the technique called smooth and synthetic oversampling technique with edited nearest neighbor which is basically it\'s just oversampling and undersampling the data sets it helps with the accuracy\"}'),
(9, 26, 'tmpvy7cdjfc.webm', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Explain how to implement dropout in a TensorFlow model and the effect it has on training.\", \"Answer\": \" explain how to implement dropout in? oh ok, dropout in, test on flow model and test on training previously i also have implement the dropout layer also in the project submission within this certifications and we can just add the dropout layer for example, if i\'m not mistaken, i have used this dropout layer in the one that the case is image classifications, german traffic something if i\'m not wrong, i have used this dropout in the middle of the layer so there is a flattened layer not flattened the convolutional layer and the flattened layer and I use that dropout layer which is I use with the rate of 0.2 or 0.5 if I\'m not wrong and then the dense layer and the last the output layer right the effect is it will really helps to improve our accuracy and lower our validation loss by turning off some of the previous layer yeah for example like we have dense layer 64 and the next layer we implement the dropout layer with the rate of 0.5 and it will turn off randomly each epoch of the previous dense layer\"}'),
(10, 26, 'tmpo3b6canp.webm', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Describe the process of building a convolutional neural network (CNN) using TensorFlow for image classification.\", \"Answer\": \" describe the process of building or configuration of your image as fiction okay the CNN one right so at the first time of course we need to make sure there are split the image folder split it for for each class okay and then we can use Keras preprocessing, if I\'m not mistaken, image dataset from directory to split the training and the validation dataset, right? yeah of course we can use another another set which is the test dataset, yeah, but yeah okay the next one we can just maybe we need to implement also the image augmentation data image augmentation to make our dataset more veritive for example like we can rotate, we can zoom it we can crop it, and the last thing of course we can build our gen model with the conventional 2D, specify the filters, the kernel size, the LRF division of course, the input shape for the first layer and then we can apply the max pooling 2d, and the next layer we can just use convolutional 2d, max pooling and whatever it is, and after that we apply the flatten layer and the last thing don\'t forget to use the dance layer for the output\"}'),
(40, 35, 'interview_question_1', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Can you share any specific challenges you faced while working on certification and how you overcame them?\", \"Answer\": \" Can you share any specific challenges you faced while working on certification and how you overcome them? Ah, okay, actually, for the challenges, there are some challenges when I took the certification, especially for the project I mentioned that I already working with it. the first one is actually to meet the specific accuracy or fallition loss for the evaluation matrix and yeah actually that just need to take some trial and error with different architecture for example like we can try to add more layer, more neurons, changes the neurons or even I also apply the dropout layer so yeah it really helps with the the validation loss to to become more lower right and yeah I think that\'s that\'s one of the biggest challenges that I have while working on these certifications\"}'),
(41, 35, 'interview_question_2', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Can you describe your experience with transfer learning in TensorFlow? How did it benefit your projects?\", \"Answer\": \" can you describe your experience with transfer learning and time short flow? how do you benefit from projects? about transfer learning is actually we use existing train model from time short flow for example like VGC16, VGC19 especially for some cases that we need to use deep learning using Keras applications for example like image classification we can use transfer learning models which is that\'s already trained model with exceptionally high accuracy high performance yeah even though it\'s trained with different data sets but it really helps to improve our model performance, model accuracy, model loss and for example like mobile net, VGG19, VGG16, efficient net, it will help to improve our models comparing to the one if you use a traditional CNN model yeah CNN model with the convolutional 2d yeah max pooling and yeah it it\'s it\'s quite good actually to use transfer learning it really helps with our model performance to improve our model performance.\"}'),
(42, 35, 'interview_question_3', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Describe a complex TensorFlow model you have built and the steps you took to ensure its accuracy and efficiency.\", \"Answer\": \" wait what is this? describe a complex TensorFlow model you have built and the steps you took to ensure its accuracy and efficiency hmmm... complex TensorFlow model you have built and steps you took to ensure its accuracy okay I will take one of my previous project that I use yeah I also use Keras or TensorFlow model it\'s it is about a cellular disease prediction yeah yeah this is also I use the research project for my undergraduate thesis yeah for my script C and I use this model it\'s quite challenging even though it\'s achieved high accuracy with some dense layer yeah with some drawout layer and trial and error also with the callback function with the neurons but the problem is the dataset is not balanced so it has the imbalanced class datasets and the approach that I use is to just to use the technique called smooth and synthetic oversampling technique with edited nearest neighbor which is basically it\'s just oversampling and undersampling the data sets it helps with the accuracy\"}'),
(43, 35, 'interview_question_4', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Explain how to implement dropout in a TensorFlow model and the effect it has on training.\", \"Answer\": \" explain how to implement dropout in? oh ok, dropout in, test on flow model and test on training previously i also have implement the dropout layer also in the project submission within this certifications and we can just add the dropout layer for example, if i\'m not mistaken, i have used this dropout layer in the one that the case is image classifications, german traffic something if i\'m not wrong, i have used this dropout in the middle of the layer so there is a flattened layer not flattened the convolutional layer and the flattened layer and I use that dropout layer which is I use with the rate of 0.2 or 0.5 if I\'m not wrong and then the dense layer and the last the output layer right the effect is it will really helps to improve our accuracy and lower our validation loss by turning off some of the previous layer yeah for example like we have dense layer 64 and the next layer we implement the dropout layer with the rate of 0.5 and it will turn off randomly each epoch of the previous dense layer\"}'),
(44, 35, 'interview_question_5', '{\"banyak_orang_terdeteksi\": 0, \"final\": \"TIDAK_MENCURIGAKAN\"}', '{\"Question\": \"Describe the process of building a convolutional neural network (CNN) using TensorFlow for image classification.\", \"Answer\": \" describe the process of building or configuration of your image as fiction okay the CNN one right so at the first time of course we need to make sure there are split the image folder split it for for each class okay and then we can use Keras preprocessing, if I\'m not mistaken, image dataset from directory to split the training and the validation dataset, right? yeah of course we can use another another set which is the test dataset, yeah, but yeah okay the next one we can just maybe we need to implement also the image augmentation data image augmentation to make our dataset more veritive for example like we can rotate, we can zoom it we can crop it, and the last thing of course we can build our gen model with the conventional 2D, specify the filters, the kernel size, the LRF division of course, the input shape for the first layer and then we can apply the max pooling 2d, and the next layer we can just use convolutional 2d, max pooling and whatever it is, and after that we apply the flatten layer and the last thing don\'t forget to use the dance layer for the output\"}');

-- --------------------------------------------------------

--
-- Table structure for table `interview`
--

CREATE TABLE `interview` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `candidate_id` int(11) NOT NULL,
  `result` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interview`
--

INSERT INTO `interview` (`id`, `user_id`, `candidate_id`, `result`, `status`, `created_at`) VALUES
(26, 3, 1, '  \"minScore\": 0,\n  \"maxScore\": 4,\n  \"scores\": [\n    {\n      \"id\": 1,\n      \"score\": 4\n    },\n    {\n      \"id\": 2,\n      \"score\": 4\n    },\n    {\n      \"id\": 3,\n      \"score\": 4\n    },\n    {\n      \"id\": 4,\n      \"score\": 4\n    },\n    {\n      \"id\": 5,\n      \"score\": 4\n    }\n  ],\n  \"communication_score\": 85,\n  \"english_fluency_score\": 80,\n  \"content_quality_score\": 95', 'Succeed', '2025-12-10 17:03:35'),
(35, 13, 1, '{\"minScore\": 0, \"maxScore\": 4, \"scores\": [{\"id\": 1, \"score\": 4}, {\"id\": 2, \"score\": 4}, {\"id\": 3, \"score\": 4}, {\"id\": 4, \"score\": 4}, {\"id\": 5, \"score\": 4}], \"communication_score\": 85, \"english_fluency_score\": 80, \"content_quality_score\": 95}', 'Succeed', '2025-12-11 14:07:49');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(300) NOT NULL,
  `password` varchar(100) NOT NULL,
  `full_name` varchar(300) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `email`) VALUES
(3, 'Sarah', '$2b$12$9i3EkcnbHPKR.RNeNT4KXOP3FkqgQnyuVh9vU7IZCjFtpVs3e2Vl.', 'Sarah Aryandi Nugrahaeni', 'sarah@gmail.com'),
(13, 'Capstone', '$2b$12$OqjOkjS6Rr6nSSYkesvmSubTJ7P80B5rcl75GnregpUzht7scY7Te', 'Capstone Jaya', 'capstone@gmail.com'),
(14, 'Mia', '$2b$12$AaPom/n1a9IWIpKEJwkZ0eAAWkrs08d06CD6G9pf3tpq/Pn.sBGQm', 'Mia and Me', 'mia@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `final_result`
--
ALTER TABLE `final_result`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_interview2` (`interview_id`);

--
-- Indexes for table `input`
--
ALTER TABLE `input`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_interview` (`interview_id`);

--
-- Indexes for table `interview`
--
ALTER TABLE `interview`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_candidate` (`candidate_id`),
  ADD KEY `fk_user` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UQ_username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `candidates`
--
ALTER TABLE `candidates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `final_result`
--
ALTER TABLE `final_result`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `input`
--
ALTER TABLE `input`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `interview`
--
ALTER TABLE `interview`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `final_result`
--
ALTER TABLE `final_result`
  ADD CONSTRAINT `fk_interview2` FOREIGN KEY (`interview_id`) REFERENCES `interview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `input`
--
ALTER TABLE `input`
  ADD CONSTRAINT `fk_interview` FOREIGN KEY (`interview_id`) REFERENCES `interview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `interview`
--
ALTER TABLE `interview`
  ADD CONSTRAINT `fk_candidate` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
