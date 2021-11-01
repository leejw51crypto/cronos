. ./setup.sh
echo 'config'$CONFIG
echo 'data'$DATA
python3 -m pystarport.cli init --config $CONFIG --data $DATA --base_port 26650
supervisord -c $DATA/tasks.ini
