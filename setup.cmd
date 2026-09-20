@echo off

mkdir docs\Roadmap
mkdir notebooks\customer
mkdir notebooks\helpers
mkdir notebooks\person
mkdir notebooks\records

call :create_notebook notebooks\customer generate_customer
call :create_notebook notebooks\helpers generate_name
call :create_notebook notebooks\helpers generate_email
call :create_notebook notebooks\helpers generate_address
call :create_notebook notebooks\helpers generate_phone
call :create_notebook notebooks\helpers generate_document
call :create_notebook notebooks\person generate_person
call :create_notebook notebooks\records generate_record

echo.
echo Done.
exit /b


:create_notebook
(
echo {
echo  "cells": [
echo   {
echo    "cell_type": "code",
echo    "execution_count": 0,
echo    "metadata": {
echo     "application/vnd.databricks.v1+cell": {
echo      "cellMetadata": {},
echo      "nuid": "",
echo      "showTitle": false,
echo      "tableResultSettingsMap": {},
echo      "title": ""
echo     }
echo    },
echo    "outputs": [],
echo    "source": []
echo   }
echo  ],
echo  "metadata": {
echo   "application/vnd.databricks.v1+notebook": {
echo    "computePreferences": null,
echo    "dashboards": [],
echo    "environmentMetadata": {
echo     "base_environment": "",
echo     "environment_version": "5"
echo    },
echo    "inputWidgetPreferences": null,
echo    "language": "python",
echo    "notebookMetadata": {
echo     "pythonIndentUnit": 4
echo    },
echo    "notebookName": "%~2",
echo    "widgets": {}
echo   },
echo   "language_info": {
echo    "name": "python"
echo   }
echo  },
echo  "nbformat": 4,
echo  "nbformat_minor": 0
echo }
) > "%~1\%~2.ipynb"

pause