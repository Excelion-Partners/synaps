# ****************** ARM ****************
ARTIFACT_PATH="../dev"

rm -rf $ARTIFACT_PATH
echo "copying files to " $ARTIFACT_PATH

mkdir $ARTIFACT_PATH

# get rid of git bindings
git archive master | tar -x -C $ARTIFACT_PATH
cd $ARTIFACT_PATH


git init
git add . -A
git checkout -b "master"
git config user.name "circleci"
git config user.email "rmoore@excelionit.com"
git commit -m "build"

# git remote add resin-upboard gh_rymoore@git.resin.io:gh_rymoore/blackboxupboarddev.git
# git remote add resin-upboard-prod gh_rymoore@git.resin.io:gh_rymoore/blackboxupboard.git
git remote add resin gh_rymoore@git.resin.io:gh_rymoore/synapsdemo.git
#git remote add resin-nuc gh_rymoore@git.resin.io:gh_rymoore/blackboxnucdev.git

git push -f resin master