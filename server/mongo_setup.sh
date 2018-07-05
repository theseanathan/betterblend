echo 'Starting mongo setup script.'
echo '\tUpdating brew...'
brew update
echo '\tInstalling mongodb...'
brew install mongodb
echo '\tSetting database ACLs...'
sudo mkdir -m 777 -p /data/db
echo 'Mongo setup script complete.'
