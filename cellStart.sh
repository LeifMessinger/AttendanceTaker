pushd app

./setupEnv.sh

echo "It's actually running at http://$(hostname -I | tr -d ' '):8000/"

./start.sh

popd
