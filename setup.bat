@echo Setup will proceed to install the necessary libraries
@pause

py -3 -m pip install -U discord
py -3 -m pip install -U requests

@echo.
@echo.
@echo Please check the results
@pause

@echo.
@set /p token=Enter your bot's token to be set as env variable:
@setx RNGSUS_TOKEN %token%
@pause