/* Creates application databases on the SQL Server instance (run as SA via db-init container). */
SET NOCOUNT ON;

IF DB_ID(N'DeutschDB') IS NULL
BEGIN
    CREATE DATABASE DeutschDB;
END;
