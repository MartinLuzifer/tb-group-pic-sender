echo "stop container: "
docker container stop tgb
echo "remove container: "
docker container rm -f tgb
echo "remove image: "
docker image rm -f tgb-pic-sender
