-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-07-2022 a las 03:58:43
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_cento_medico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tb_citas`
--

CREATE TABLE `tb_citas` (
  `id_cita` int(11) NOT NULL,
  `id_expediente` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Peso` decimal(10,0) NOT NULL,
  `Altura` int(3) NOT NULL,
  `Temperatura` int(2) NOT NULL,
  `Latidos` int(11) NOT NULL,
  `Saturacion_oxigeno` int(11) NOT NULL,
  `Glucosa` int(11) NOT NULL,
  `Edad` int(11) NOT NULL,
  `Sintomas` varchar(300) NOT NULL,
  `Diagnostico` varchar(300) NOT NULL,
  `Tratamiento` varchar(250) NOT NULL,
  `Estudios` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tb_doctores`
--

CREATE TABLE `tb_doctores` (
  `id_doctor` int(11) NOT NULL,
  `RFC` varchar(13) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Cedula` int(7) NOT NULL,
  `Correo` varchar(45) NOT NULL,
  `Password` varchar(110) NOT NULL,
  `Rol` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tb_doctores`
--

INSERT INTO `tb_doctores` (`id_doctor`, `RFC`, `Nombre`, `Cedula`, `Correo`, `Password`, `Rol`) VALUES
(14, 'PAPA001001M97', 'jose antonio patiño palomares', 7623947, 'joseantonio15826@gmail.com', '$pbkdf2-sha256$30000$gRBiDEEohXCOMcZ4z7kXAg$QNP8bLGqTfNLYvrTNccSi6vCoWkkubmb2zMr7FvY18A', 2),
(15, 'JAJK980617884', 'karla jaramillo juarez', 8712309, 'karlajuarez9@gmail.com', '$pbkdf2-sha256$30000$HKP0fs/Zm3Mu5dxb652Tkg$oW1.ZCjJxTAYLOtnCybBBIGzwZXIPoYD.9wA4iPklsg', 1),
(17, 'REMI0006136X7', 'ismael martinez martinez', 9998276, 'ismael2@gmail.com', '$pbkdf2-sha256$30000$Zsw55xyj9J4TIiTkfK/1Hg$Lbi5rapOdisi2OMJt1LeCzDYYdBiwrwU7Z8Q0.jnEFo', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tb_expedientes`
--

CREATE TABLE `tb_expedientes` (
  `id_expediente` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `Nombre` varchar(120) NOT NULL,
  `Fecha_nacimiento` date NOT NULL,
  `Enfermedades` varchar(200) NOT NULL DEFAULT 'no',
  `Alergias` varchar(200) DEFAULT 'no',
  `Antecedentes` varchar(150) DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tb_expedientes`
--

INSERT INTO `tb_expedientes` (`id_expediente`, `id_doctor`, `Nombre`, `Fecha_nacimiento`, `Enfermedades`, `Alergias`, `Antecedentes`) VALUES
(1, 14, 'juan antonio morales', '2000-06-06', 'ta medio wey', 'al estudio', 'nada');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tb_citas`
--
ALTER TABLE `tb_citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `id_expediente` (`id_expediente`),
  ADD KEY `id_doctor` (`id_doctor`);

--
-- Indices de la tabla `tb_doctores`
--
ALTER TABLE `tb_doctores`
  ADD PRIMARY KEY (`id_doctor`);

--
-- Indices de la tabla `tb_expedientes`
--
ALTER TABLE `tb_expedientes`
  ADD PRIMARY KEY (`id_expediente`),
  ADD KEY `id_doctor` (`id_doctor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tb_citas`
--
ALTER TABLE `tb_citas`
  MODIFY `id_cita` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tb_doctores`
--
ALTER TABLE `tb_doctores`
  MODIFY `id_doctor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `tb_expedientes`
--
ALTER TABLE `tb_expedientes`
  MODIFY `id_expediente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tb_citas`
--
ALTER TABLE `tb_citas`
  ADD CONSTRAINT `tb_citas_ibfk_1` FOREIGN KEY (`id_expediente`) REFERENCES `tb_expedientes` (`id_expediente`) ON UPDATE CASCADE,
  ADD CONSTRAINT `tb_citas_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `tb_doctores` (`id_doctor`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `tb_expedientes`
--
ALTER TABLE `tb_expedientes`
  ADD CONSTRAINT `tb_expedientes_ibfk_1` FOREIGN KEY (`id_doctor`) REFERENCES `tb_doctores` (`id_doctor`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
