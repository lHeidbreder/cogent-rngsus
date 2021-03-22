echo Setup will proceed to install the necessary libraries
echo Press any key to confirm
read -n 1 -s

pip install discord
pip install requests

echo -e "\n\nPlease confirm the results"
read -n 1 -s