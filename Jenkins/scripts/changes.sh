preCommit=$1
currentCommit=$2
echo $(git diff $preCommit $currentCommit --name-only | tr '\n' '-')