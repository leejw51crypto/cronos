. ./setup.sh
echo 'config'$CONFIG
echo 'data'$DATA
pystarport init --config $CONFIG --data $DATA --base_port 26650
supervisord -c $DATA/tasks.ini
